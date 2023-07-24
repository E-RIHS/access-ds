<script>
import WTitlebanner from '@/components/WTitlebanner.vue'
import api from '@/utils/request'

export default {
    name: 'SchemaConfigIndexPage',
    components: {
        WTitlebanner,
    },
    data() {
        return {
            configs: [],
            tableHeaders: [
                { text: '', value: 'id', sortable: false},
                { text: 'Name', value: 'name' },
                { text: 'Resource', value: 'resource' },
                { text: 'Category', value: 'category' },
                { text: 'JSON schema', value: 'json_schema' },
                { text: 'UI schema', value: 'ui_schema' },
                { text: 'Default dataset', value: 'default_dataset' },
            ],
            tableOptions: {
                "sortBy": ['name'],
                "sortDesc": [false],
                "multiSort": true,
            },
            tableLoading: true,
            tableTotal: 0
        }
    },

    mounted() {
        //this.getConfigs()
    },

    watch: {
        tableOptions() {
            this.getConfigs()
        },
    },

    methods: {
        getConfigs() {
            this.tableLoading = true

            // query parameters
            let skip = (this.tableOptions.page - 1) * this.tableOptions.itemsPerPage
            let parameters = {
                skip: isNaN(skip) ? null : skip,
                limit: this.tableOptions.itemsPerPage,
                sort_by: this.tableOptions.sortBy,
                sort_desc: this.tableOptions.sortDesc
            }

            // api call
            console.log('GET /schema_config/')
            api.get('/schema_config/', {params: parameters})
                .then(response => {
                    this.configs = response.data.data
                    this.tableTotal = response.data.query_parameters.total
                    this.tableLoading = false
                    this.getAllSchemaNames()
                })
                .catch(error => {
                    console.warn(error)
                })
        },
        
        getAllSchemaNames() {
            const schemaTypes = ["json_schema", "ui_schema", "i18n_schema", "default_dataset"]

            for (let i = 0; i < this.configs.length; i++) {
                for (const schemaType of schemaTypes) {
                    if (schemaType in this.configs[i]) {
                        let id = this.configs[i][schemaType]
                        if (id) {
                            let url = '/' + schemaType + '/' + id + '/name'
                            console.log('GET ' + url)
                            api.get(url)
                                .then(response => {
                                    this.configs[i][schemaType] = response.data.name
                                })
                                .catch(error => {
                                    console.warn(error)
                                })
                        }
                    }
                }
            }
        },
    }
}
</script>

<template>
    <div>
        <w-titlebanner title="Schema configurations"></w-titlebanner>

        <v-container>
            <v-data-table
                :headers="tableHeaders"
                :items="configs"
                :server-items-length="tableTotal"
                :options.sync="tableOptions"
                :loading="tableLoading"
                :footer-props="{'items-per-page-options':[10, 50, 100, -1]}"
                class="elevation-2">
                <template v-slot:item.id="{ item }">
                    <v-tooltip top>
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                icon
                                color="primary"
                                class="mr-2"
                                :to="'/admin/schema/' + item.id"
                                v-bind="attrs"
                                v-on="on">
                                <v-icon>mdi-code-json</v-icon>
                            </v-btn>
                        </template>
                        <span>Open configuration</span>
                    </v-tooltip>
                </template>
            </v-data-table>
        </v-container>
    </div>
</template>