<script>
import WTitlebanner from '@/components/WTitlebanner.vue'
import api from '@/utils/request'

export default {
    name: 'SchemaConfigPage',
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
            tableLoading: true
        }
    },
    mounted() {
        this.getConfigs()
    },
    methods: {
        getConfigs() {
            console.log('GET /schema_config/')
            api.get('/schema_config/')
            .then(response => {
                this.configs = response.data.data
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
                :loading="tableLoading"
                class="elevation-2"
            ></v-data-table>
            <pre>{{ configs }}</pre>
        </v-container>
    </div>
</template>