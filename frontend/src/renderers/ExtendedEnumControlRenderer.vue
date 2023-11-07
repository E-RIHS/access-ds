<template>
    <control-wrapper
        v-bind="controlWrapper"
        :styles="styles"
        :isFocused="isFocused"
        :appliedOptions="appliedOptions"
    >
        <v-hover v-slot="{ hover }">
            <v-select
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
                :clearable="hover"
                :value="control.data"
                :items="control.options"
                :item-text="(item) => t(item.label, item.label)"
                item-value="value"
                v-bind="vuetifyProps('v-select')"
                @change="onChange"
                @focus="isFocused = true"
                @blur="isFocused = false"
            />
        </v-hover>
    </control-wrapper>
</template>
  
<script>
import { isEnumControl, rankWith } from '@jsonforms/core'
import { rendererProps, useJsonFormsEnumControl } from '@jsonforms/vue2'
import { defineComponent } from 'vue'
import { VHover, VSelect } from 'vuetify/lib'
import { ControlWrapper, useTranslator, useVuetifyControl, DisabledIconFocus } from '@jsonforms/vue2-vuetify'

const controlRenderer = defineComponent({
    name: 'extended-enum-control-renderer',
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

    mounted() {
        console.log("extended-enum-control-renderer mounted")
    },
})
  
export default controlRenderer
  
export const entry = {
    renderer: controlRenderer,
    tester: rankWith(20, isEnumControl),
}

</script>