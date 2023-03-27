<script>
import { JsonForms } from '@jsonforms/vue2'
import { vuetifyRenderers, additionalRenderers } from '@jsonforms/vue2-vuetify'
import { createAjv, Generate } from '@jsonforms/core'

import WTitlebanner from '@/components/WTitlebanner.vue'
import WJsonEditor from '@/components/WJsonEditor.vue'
import api from '@/utils/request'

const renderers = [...vuetifyRenderers, ...additionalRenderers]

const configJsonSchema = {
    title: 'SchemaConfig',
    type: 'object',
    properties: {
        id: { title: 'Id', type: 'string' },
        name: {
            title: 'Name',
            description: 'Short descriptive name',
            maxLength: 100,
            minLength: 1,
            type: 'string',
        },
        resource: {
            title: 'Resource',
            description: 'An enumeration.',
            enum: ['Examination', 'Service', 'Project'],
            type: 'string',
        },
        category: {
            title: 'Category',
            description: 'Category identifier',
            maxLength: 20,
            minLength: 1,
            type: 'string',
        },
        json_schema: { title: 'Json Schema', type: 'string' },
        ui_schema: { title: 'Ui Schema', type: 'string' },
        i18n_schema: { title: 'I18N Schema', type: 'string' },
        default_dataset: { title: 'Default Dataset', type: 'string' },
        draft: { title: 'Draft', default: false, type: 'boolean' },
        depreciated: { title: 'Depreciated', default: false, type: 'boolean' },
    },
    required: ['name', 'resource', 'json_schema'],
}

const configUiSchema = {
    type: 'VerticalLayout',
    elements: [
        {
            type: 'HorizontalLayout',
            elements: [
                {
                    type: 'Control',
                    scope: '#/properties/name',
                },
                {
                    type: 'Control',
                    scope: '#/properties/resource',
                },
                {
                    type: 'Control',
                    scope: '#/properties/category',
                },
            ],
        },
        {
            type: 'HorizontalLayout',
            elements: [
                {
                    type: 'Control',
                    scope: '#/properties/json_schema',
                },
                {
                    type: 'Control',
                    scope: '#/properties/ui_schema',
                },
                {
                    type: 'Control',
                    scope: '#/properties/i18n_schema',
                },
                {
                    type: 'Control',
                    scope: '#/properties/default_dataset',
                },
            ],
        },
        {
            type: 'HorizontalLayout',
            elements: [
                {
                    type: 'Control',
                    scope: '#/properties/draft',
                },
                {
                    type: 'Control',
                    scope: '#/properties/depreciated',
                },
            ],
        },
    ],
}

export default {
    name: 'SchemaConfigDetailPage',
    components: {
        WTitlebanner,
        WJsonEditor,
        JsonForms,
    },

    data() {
        return {
            id: this.$route.params.id,
            config: {},
            configJsonSchema: configJsonSchema,
            configUiSchema: configUiSchema,
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
            isValid: false,
            editorOptions: {
                mode: 'tree', // text, code, tree (default), form, preview (ro), view (ro),
                modes: ['tree', 'code', 'text'],
                //name: "test"
            },
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
                .then((response) => {
                    this.config = response.data
                    if ('category' in this.config && this.config.category == null) {
                        delete this.config['category']
                    }
                    if ('ui_schema' in this.config && this.config.ui_schema == null) {
                        delete this.config['ui_schema']
                    }
                    if ('i18n_schema' in this.config && this.config.i18n_schema == null) {
                        delete this.config['i18n_schema']
                    }
                    if ('default_dataset' in this.config && this.config.default_dataset == null) {
                        delete this.config['default_dataset']
                    }
                    this.jsonSchema = this.config['json_schema_resolved']
                        ? this.config['json_schema_resolved']
                        : {}
                    delete this.config['json_schema_resolved']
                    this.uiSchema = this.config['ui_schema_resolved']
                        ? this.config['ui_schema_resolved']
                        : undefined
                    delete this.config['ui_schema_resolved']
                    this.i18nSchema = this.config['i18n_schema_resolved']
                        ? this.config['i18n_schema_resolved']
                        : undefined
                    delete this.config['i18n_schema_resolved']
                    this.defaultDataset = this.config[
                        'default_dataset_resolved'
                    ]
                        ? this.config['default_dataset_resolved']
                        : undefined
                    this.instance = this.config['default_dataset_resolved']
                        ? JSON.parse(
                              JSON.stringify(
                                  this.config['default_dataset_resolved']
                              )
                          )
                        : {}
                    delete this.config['default_dataset_resolved']
                })
                .catch((error) => {
                    console.warn(error)
                })
        },

        onConfigChange(event) {
            this.config = event.data
            //this.isValid = (event.errors.length === 0)
        },

        onInstanceChange(event) {
            this.instance = event.data
            this.isValid = event.errors.length === 0
        },

        generateUISchema() {
            this.uiSchema = Generate.uiSchema(this.jsonSchema)
        },

        removeUISchema() {
            this.uiSchema = undefined
            if ('ui_schema' in this.config) {
                this.config.ui_schema = undefined
                console.log(this.config.ui_schema)
            }
        },

        overwriteUISchema() {},
        saveNewUISchema() {},
    },
}
</script>

<template>
    <div>
        <w-titlebanner
            :title="'name' in config ? config['name'] : 'New'"
        ></w-titlebanner>

        <v-container>
            <json-forms
                :renderers="renderers"
                :data="config"
                :schema="configJsonSchema"
                :uischema="configUiSchema"
                :i18n="undefined"
                :ajv="ajv"
                @change="onConfigChange"
            ></json-forms>
        </v-container>

        <v-container fluid>
            <v-row>
                <v-col>
                    <v-card>
                        <v-card-title>
                            <v-tabs v-model="schemaTab" grow>
                                <v-tab>JSON Schema</v-tab>
                                <v-tab>UI Schema</v-tab>
                                <v-tab>I18n Schema</v-tab>
                                <v-tab>Default dataset</v-tab>
                            </v-tabs>
                        </v-card-title>
                        <v-card-text v-if="schemaTab === 0">
                            <w-json-editor
                                v-model="jsonSchema"
                                :plus="true"
                                :options="editorOptions"
                                height="600px"
                            ></w-json-editor>
                        </v-card-text>
                        <v-card-text v-if="schemaTab === 1">
                            <v-card elevation="0">
                                <v-card-text>
                                    <w-json-editor
                                        v-if="uiSchema !== undefined"
                                        v-model="uiSchema"
                                        :plus="true"
                                        :options="editorOptions"
                                        height="600px"
                                    ></w-json-editor>
                                    <div 
                                        v-else
                                        class="ma-4 font-italic">
                                        <strong>No UI Schema defined.</strong><br />
                                        Select an existing UI Schema (above), or generate a basic UI Schema based on the JSON Schema.
                                        This <a href="https://jsonforms-editor.netlify.app/" target="_blank"><v-icon x-small color="primary">mdi-open-in-new</v-icon>tool</a> provides a visual UI Schema builder. 
                                    </div>
                                </v-card-text>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <div v-if="uiSchema !== undefined">
                                        <v-btn
                                            class="ma-2"
                                            @click="removeUISchema()">
                                            Wipe
                                        </v-btn>
                                        <v-btn
                                            class="ma-2"
                                            @click="overwriteUISchema()">
                                            Save
                                        </v-btn>
                                        <v-btn
                                            color="primary"
                                            class="ma-2"
                                            @click="saveNewUISchema()">
                                            Save as new...
                                        </v-btn>
                                    </div>
                                    <v-btn
                                        v-else
                                        color="primary"
                                        class="ma-2"
                                        @click="generateUISchema()">
                                        Generate UI Schema
                                    </v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-card-text>
                        <v-card-text v-if="schemaTab === 2">
                            <w-json-editor
                                v-if="i18nSchema !== undefined"
                                v-model="i18nSchema"
                                :plus="true"
                                :options="editorOptions"
                                height="600px"
                            ></w-json-editor>
                        </v-card-text>
                        <v-card-text v-if="schemaTab === 3">
                            <w-json-editor
                                v-if="defaultDataset !== undefined"
                                v-model="defaultDataset"
                                :plus="true"
                                :options="editorOptions"
                                height="600px"
                            ></w-json-editor>
                        </v-card-text>
                    </v-card>
                </v-col>
                <v-col>
                    <v-card>
                        <v-card-title>
                            <v-tabs v-model="instanceTab" grow>
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
                                @change="onInstanceChange"
                            ></json-forms>
                        </v-card-text>
                        <v-card-text v-if="instanceTab === 1">
                            <w-json-editor
                                v-model="instance"
                                :plus="true"
                                :options="editorOptions"
                                height="600px"
                            ></w-json-editor>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
        <pre>{{ JSON.stringify(config, " ", 2) }}</pre>
    </div>
</template>
