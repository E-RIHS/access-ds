<template>
    <control-wrapper
        v-bind="controlWrapper"
        :styles="styles"
        :isFocused="isFocused"
        :appliedOptions="appliedOptions"
    >
        <v-hover v-slot="{ hover }">
            <v-combobox
                v-if="items !== undefined"
                v-disabled-icon-focus
                :id="control.id + '-input'"
                :class="styles.control.input"
                :disabled="!control.enabled"
                :autofocus="appliedOptions.focus"
                :placeholder="appliedOptions.placeholder"
                :label="computedLabel"
                :hint="control.description"
                :persistent-hint="persistentHint()"
                :required="control.required"
                :error-messages="control.errors"
                :maxlength="
                    appliedOptions.restrict
                        ? control.schema.maxLength
                        : undefined
                "
                :counter="
                    control.schema.maxLength !== undefined
                        ? control.schema.maxLength
                        : undefined
                "
                :clearable="hover"
                :value="control.data"   
                :items="items"
                :item-text="itemTitle"      
                :item-value="itemValue"
                :return-object="false"
                hide-no-data
                v-bind="vuetifyProps('v-combobox')"
                @input="onChange"
                @focus="isFocused = true"
                @blur="isFocused = false"
            />
            <v-text-field
                v-else
                v-disabled-icon-focus
                :id="control.id + '-input'"
                :class="styles.control.input"
                :disabled="!control.enabled"
                :autofocus="appliedOptions.focus"
                :placeholder="appliedOptions.placeholder"
                :label="computedLabel"
                :hint="control.description"
                :persistent-hint="persistentHint()"
                :required="control.required"
                :error-messages="control.errors"
                :value="control.data"
                :maxlength="
                    appliedOptions.restrict
                        ? control.schema.maxLength
                        : undefined
                "
                :counter="
                    control.schema.maxLength !== undefined
                        ? control.schema.maxLength
                        : undefined
                "
                :clearable="hover"
                v-bind="vuetifyProps('v-text-field')"
                @input="onChange"
                @focus="isFocused = true"
                @blur="isFocused = false"
            />
        </v-hover>
    </control-wrapper>
</template>

<script>
import { rankWith, isStringControl } from '@jsonforms/core'
import { defineComponent } from 'vue'
import { rendererProps, useJsonFormsControl } from '@jsonforms/vue2'
import { ControlWrapper } from '@jsonforms/vue2-vuetify'
import { useVuetifyControl } from '@jsonforms/vue2-vuetify'
import { VHover, VTextField, VCombobox } from 'vuetify/lib'
import { DisabledIconFocus } from '@jsonforms/vue2-vuetify'
import isArray from 'lodash/isArray'
import every from 'lodash/every'
import isString from 'lodash/isString'
import axios from 'axios'

const controlRenderer = defineComponent({
    name: 'extended-string-control-renderer',
    components: {
        ControlWrapper,
        VHover,
        VTextField,
        VCombobox,
    },
    directives: {
        DisabledIconFocus,
    },
    props: {
        ...rendererProps(),
    },
    setup(props) {
        return useVuetifyControl(
            useJsonFormsControl(props),
            (value) => value || undefined,
            300
        )
    },
    data() {
        return {
            items: undefined,
            itemTitle: 'label',     // note: vuetify2: item-text, vuetify3: item-title
            itemValue: 'label',     // note: not possible to store id's and display labels in combobox (see https://github.com/vuetifyjs/vuetify/issues/5479)
        }
    },
    methods: {
        getItems() {
            const uiSuggestions = this.control.uischema.options?.suggestion
            if ( uiSuggestions !== undefined && isArray(uiSuggestions) && every(uiSuggestions, isString)) {
                this.items = uiSuggestions
                return
            }

            const uiExamplesApi = this.control.uischema.options?.examples_api
            if ( uiExamplesApi !== undefined ) {
                axios.get(uiExamplesApi)
                    .then((response) => {
                        if (this.control.uischema.options?.examples_api_id !== undefined)
                            this.itemValue = this.control.uischema.options?.examples_api_id
                        if (this.control.uischema.options?.examples_api_label !== undefined)
                            this.itemTitle = this.control.uischema.options?.examples_api_label
                        this.items = response.data.data
                        return
                    })
                    .catch((error) => {console.log(error)})
            }
            
            const uiExamples = this.control.uischema.options?.examples
            if ( uiExamples !== undefined && isArray(uiExamples) && every(uiExamples, isString)) {
                this.items = uiExamples
                return
            }

            const jsonExamplesApi = this.control.schema.examples_api
            if ( jsonExamplesApi !== undefined ) {
                axios.get(jsonExamplesApi)
                    .then((response) => {
                        if (this.control.schema.examples_api_id !== undefined)
                            this.itemValue = this.control.schema.examples_api_id
                        if (this.control.schema.examples_api_label !== undefined)
                            this.itemTitle = this.control.schema.examples_api_label
                        this.items = response.data.data
                        return
                    })
                    .catch((error) => {console.log(error)})
            }
            
            const jsonExamples = this.control.schema.examples
            if ( jsonExamples !== undefined && isArray(jsonExamples) && every(jsonExamples, isString)) {
                this.items = jsonExamples
                return
            }

            // no suggestions/examples or incorrect data
            this.items = undefined
        },
    },

    mounted() {
        this.getItems()
    },
})

export default controlRenderer

export const entry = {
    renderer: controlRenderer,
    tester: rankWith(3, isStringControl),
}

</script>
