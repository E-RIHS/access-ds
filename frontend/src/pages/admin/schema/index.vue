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
                })
                .catch(error => {
                    console.warn(error)
                })
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