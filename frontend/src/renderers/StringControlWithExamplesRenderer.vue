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
            appliedOptions.restrict ? control.schema.maxLength : undefined
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
            appliedOptions.restrict ? control.schema.maxLength : undefined
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
  
  <script lang="js">
  import { rankWith, isStringControl } from '@jsonforms/core';
  import { defineComponent } from 'vue';
  import { rendererProps, useJsonFormsControl } from '@jsonforms/vue2';
  import { ControlWrapper } from '@jsonforms/vue2-vuetify';
  import { useVuetifyControl } from '@jsonforms/vue2-vuetify';
  import { VHover, VTextField, VCombobox } from 'vuetify/lib';
  import { DisabledIconFocus } from '@jsonforms/vue2-vuetify';
  import isArray from 'lodash/isArray';
  import every from 'lodash/every';
  import isString from 'lodash/isString';
  
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
      );
    },
    computed: {
      suggestions() {
        const suggestions = this.control.uischema.options?.suggestion
        const examples = this.control.schema.examples

        console.log(suggestions)

        if (
          suggestions === undefined ||
          !isArray(suggestions) ||
          !every(suggestions, isString)
        ) {
            if (
                examples === undefined ||
                !isArray(examples) ||
                !every(examples, isString)
            ) {
                // check for incorrect data
                return undefined;
            } else {
                return examples;
        }
        } else {
            return suggestions;
        }


      },
    },
  });
  

  
  const entry = {
    renderer: controlRenderer,
    tester: rankWith(3, isStringControl),
  };

  export default entry

  </script>