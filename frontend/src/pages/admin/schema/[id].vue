<script>
import { JsonForms } from '@jsonforms/vue2'
import { vuetifyRenderers, additionalRenderers } from '@jsonforms/vue2-vuetify'
import { createAjv, Generate } from '@jsonforms/core'

import WTitlebanner from '@/components/WTitlebanner.vue'
import api from '@/utils/request'

const renderers = [...vuetifyRenderers, ...additionalRenderers]

export default {
    name: 'SchemaConfigDetailPage',
    components: {
        WTitlebanner,
        JsonForms
    },

    data() {
        return {
            id: this.$route.params.id,
            config: {},
            jsonSchema: {},
            uiSchema: {},
            i18nSchema: {},
            defaultDataset: {},
            schemaTab: 0,
            instanceTab: 0,
            dataEntry: true,
            renderers: Object.freeze(renderers),
            ajv: createAjv({ useDefaults: true }),
            instance: {},
            isValid: false
        }
    },

    mounted() {
        this.getConfig()
    },

    methods: {
        getConfig() {
            // api call
            console.log('GET /schema_config/' + this.id)
            api.get('/schema_config/' + this.id)
                .then(response => {
                    this.config = response.data
                    this.jsonSchema = this.config['json_schema_resolved'] ? 
                        this.config['json_schema_resolved'] : {}
                    delete this.config['json_schema_resolved']
                    this.uiSchema = this.config['ui_schema_resolved'] ? 
                        this.config['ui_schema_resolved'] : undefined
                    delete this.config['i18n_schema_resolved']
                    this.i18nSchema = this.config['i18n_schema_resolved'] ? 
                        this.config['i18n_schema_resolved'] : undefined
                    delete this.config['i18n_schema_resolved']
                    this.defaultDataset = this.config['default_dataset_resolved'] ? 
                        this.config['default_dataset_resolved'] : undefined
                    this.instance = this.config['default_dataset_resolved'] ? 
                        JSON.parse(JSON.stringify(this.config['default_dataset_resolved'])) : {}
                    delete this.config['default_dataset_resolved']
                })
                .catch(error => {
                    console.warn(error)
                })
        },

        onChange(event) {
            this.instance = event.data
            this.isValid = (event.errors.length === 0)
        },
    }
}
</script>

<template>
    <div>
        <w-titlebanner :title="'name' in config ? config['name'] : 'New'"></w-titlebanner>

        <v-container>
            <pre>{{ config }}</pre>
        </v-container>

        <v-container fluid>
            <v-row>
                <v-col>
                    <v-card>
                        <v-card-title>
                            <v-tabs 
                                v-model="schemaTab" 
                                grow>
                                <v-tab>JSON Schema</v-tab>
                                <v-tab>UI Schema</v-tab>
                                <v-tab>I18n Schema</v-tab>
                                <v-tab>Default dataset</v-tab>
                            </v-tabs>
                        </v-card-title>
                        <v-card-text v-if="schemaTab === 0">
                            <pre>{{ this.jsonSchema }}</pre>
                        </v-card-text>
                        <v-card-text v-if="schemaTab === 1">
                            <pre>{{ this.uiSchema }}</pre>
                        </v-card-text>
                        <v-card-text v-if="schemaTab === 2">
                            <pre>{{ this.i18nSchema }}</pre>
                        </v-card-text>
                        <v-card-text v-if="schemaTab === 3">
                            <pre>{{ this.defaultDataset }}</pre>
                        </v-card-text>
                    </v-card>
                </v-col>
                <v-col>
                    <v-card>
                        <v-card-title>
                                <v-tabs 
                                    v-model="instanceTab" 
                                    grow>
                                <v-tab>Example form</v-tab>
                                <v-tab>Example dataset</v-tab>
                            </v-tabs>
                        </v-card-title>
                        <v-card-text v-if="instanceTab === 0">
                            <json-forms
                                :renderers="renderers"
                                :data="instance"
                                :schema="jsonSchema"
                                :uischema="uiSchema"
                                :i18n="i18nSchema"
                                :ajv="ajv"
                                @change="onChange"
                            ></json-forms>
                        </v-card-text>
                        <v-card-text v-if="instanceTab === 1">
                            <pre>{{ this.instance }}</pre>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>