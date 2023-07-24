<script>
import { JsonForms } from '@jsonforms/vue2'
import { vuetifyRenderers, additionalRenderers } from '@jsonforms/vue2-vuetify'
import { createAjv, Generate } from '@jsonforms/core'
import WTitlebanner from '@/components/WTitlebanner.vue'
import api from '@/utils/request'

const renderers = [...vuetifyRenderers, ...additionalRenderers]

export default {
    name: 'GeneridFormPage',
    components: {
        JsonForms,
        WTitlebanner,
    },
    data() {
        return {
            config: null,
            renderers: Object.freeze(renderers),
            jsonSchema: undefined,
            uiSchema: undefined,
            i18nSchema: undefined,
            ajv: createAjv({ useDefaults: true }),
            title: 'New generic dataset',
            data: {},
            isValid: false,
        }
    },
    mounted() {
        this.getConfig()
    },
    methods: {
        getConfig() {
            console.log('GET /schema_config/' + this.$route.params.id)
            api.get('/schema_config/' + this.$route.params.id)
                .then((response) => {
                    this.config = response.data.id
                    this.title = "New '" + response.data.resource + "' dataset"
                    this.jsonSchema = response.data.json_schema_resolved
                    if (response.data.ui_schema_resolved) {
                        this.uiSchema = response.data.ui_schema_resolved
                    }
                    if (response.data.i18n_schema_resolved) {
                        this.i18nSchema = response.data.i18n_schema_resolved
                    }
                    if (response.data.default_dataset_resolved) {
                        this.data = response.data.default_dataset_resolved
                    }
                })
                .catch((error) => {
                    console.warn(error)
                })
        },
        onChange(event) {
            this.data = event.data
            this.isValid = event.errors.length === 0
        },
        saveGenericDataset() {
            if (this.isValid) {
                let dataset = {
                    $schema: this.jsonSchema.$id,
                    $config: this.config,
                    ...this.data,
                }
                console.log('POST /generic/')
                api.post('/generic/', dataset)
                    .then((response) => {
                        this.$router.push('/generic')
                    })
                    .catch((error) => {
                        console.warn(error)
                    })
            }
        },
    },
}
</script>

<template>
    <div>
        <w-titlebanner :title="title"></w-titlebanner>

        <v-card elevation="0">
            <json-forms
                :renderers="renderers"
                :data="data"
                :schema="jsonSchema"
                :uischema="uiSchema"
                :i18n="i18nSchema"
                :ajv="ajv"
                @change="onChange"
            ></json-forms>
        </v-card>

        <v-container>
            <v-btn
                color="primary"
                elevation="2"
                :disabled="!isValid"
                @click="saveGenericDataset"
            >
                Save
            </v-btn>
        </v-container>
    </div>
</template>
