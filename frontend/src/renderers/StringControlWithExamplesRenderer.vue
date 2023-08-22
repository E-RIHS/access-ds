<template>
    <control-wrapper
        v-bind="controlWrapper"
        :styles="styles"
        :isFocused="isFocused"
        :appliedOptions="appliedOptions"
    >
        <v-hover v-slot="{ hover }">
            <v-combobox
                v-if="suggestions !== undefined"
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
                :items="suggestions"
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
    name: 'string-control-with-examples-renderer',
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
    computed: {
        suggestions() {
            const uiSuggestions = this.control.uischema.options?.suggestion
            if ( uiSuggestions !== undefined && isArray(uiSuggestions) && every(uiSuggestions, isString)) {
                return uiSuggestions
            }

            const uiExamplesApi = this.control.uischema.options?.examples-api
            if ( uiExamplesApi !== undefined ) {
                axios.get(uiExamplesApi)
                    .then((response) => {return response.data})
                    .catch((error) => {console.log(error)})
            }
            
            const uiExamples = this.control.uischema.options?.examples
            if ( uiExamples !== undefined && isArray(uiExamples) && every(uiExamples, isString)) {
                return uiExamples
            }

            const jsonExamplesApi = this.control.schema.examples-api
            if ( jsonExamplesApi !== undefined ) {
                axios.get(jsonExamplesApi)
                    .then((response) => {return response.data})
                    .catch((error) => {console.log(error)})
            }
            
            const jsonExamples = this.control.schema.examples
            if ( jsonExamples !== undefined && isArray(jsonExamples) && every(jsonExamples, isString)) {
                return jsonExamples
            }

            // no suggestions/examples or incorrect data
            return undefined
        },
    },
})

export default controlRenderer

export const entry = {
    renderer: controlRenderer,
    tester: rankWith(3, isStringControl),
}

</script>
