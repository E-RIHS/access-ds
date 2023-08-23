<template>
    <control-wrapper v-bind="controlWrapper" :styles="styles" :isFocused="isFocused" :appliedOptions="appliedOptions">
        <v-hover v-slot="{ hover }">
            <v-select v-disabled-icon-focus :id="control.id + '-input'" :class="styles.control.input"
                :disabled="!control.enabled" :autofocus="appliedOptions.focus" :placeholder="appliedOptions.placeholder"
                :label="computedLabel" :hint="control.description" :persistent-hint="persistentHint()"
                :required="control.required" :error-messages="control.errors" :clearable="hover" :value="control.data"
                :items="items" :item-text="itemTitle" :item-value="itemValue" v-bind="vuetifyProps('v-select')"
                @change="onChange" @focus="isFocused = true" @blur="isFocused = false" />
        </v-hover>
    </control-wrapper>
</template>
  
<script>
import { isStringControl, rankWith, and, or, schemaMatches } from '@jsonforms/core'
import { rendererProps, useJsonFormsEnumControl } from '@jsonforms/vue2'
import { defineComponent } from 'vue'
import { VHover, VSelect } from 'vuetify/lib'
import { ControlWrapper, useTranslator, useVuetifyControl, DisabledIconFocus } from '@jsonforms/vue2-vuetify'
import isEmpty from 'lodash/isEmpty';

const controlRenderer = defineComponent({
    name: 'extended-enum-api-control-renderer',
    components: {
        ControlWrapper,
        VSelect,
        VHover,
    },
    directives: {
        DisabledIconFocus,
    },
    props: {
        ...rendererProps(),
    },
    setup(props) {
        const t = useTranslator();

        const control = useVuetifyControl(useJsonFormsEnumControl(props), (value) =>
            value !== null ? value : undefined
        )

        return { ...control, t }
    },

    data() {
        return {
            items: undefined,
            itemTitle: 'label',     // note: vuetify2: item-text, vuetify3: item-title
            itemValue: 'id',
        }
    },

    methods: {
        getItems() {
            const uiEnumApi = this.control.uischema.options?.enum_api
            if (uiEnumApi !== undefined) {
                axios.get(uiEnumApi)
                    .then((response) => {
                        if (this.control.uischema.options?.enum_api_id !== undefined)
                            this.itemValue = this.control.uischema.options?.enum_api_id
                        if (this.control.uischema.options?.enum_api_label !== undefined)
                            this.itemTitle = this.control.uischema.options?.enum_api_label
                        this.items = response.data.data
                        return
                    })
                    .catch((error) => { console.log(error) })
            }

            const jsonEnumApi = this.control.schema.enum_api
            if (jsonEnumApi !== undefined) {
                axios.get(jsonEnumApi)
                    .then((response) => {
                        if (this.control.schema.enum_api_id !== undefined)
                            this.itemValue = this.control.schema.enum_api_id
                        if (this.control.schema.enum_api_label !== undefined)
                            this.itemTitle = this.control.schema.enum_api_label
                        this.items = response.data.data
                        return
                    })
                    .catch((error) => { console.log(error) })
            }

            // no suggestions/examples or incorrect data
            this.items = undefined
        },
    },

    mounted() {
        this.getItems()
        console.log("extended-enum-api-control-renderer mounted")
    },
})

export default controlRenderer

const hasOption =
    (optionName) =>
        (uischema) => {
            if (isEmpty(uischema)) {
                return false
            }

            const options = uischema.options;
            return (
                (options &&
                    !isEmpty(options) &&
                    typeof options[optionName] === 'string') ||
                false
            )
        }

export const entry = {
    renderer: controlRenderer,
    tester: rankWith(4, and(
        isStringControl,
        or(
            schemaMatches((schema) => Object.prototype.hasOwnProperty.call(schema, 'enum_api')),
            hasOption('enum_api')
        )
    )
    ),
}

</script>