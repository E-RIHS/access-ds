<script>
import WTitlebanner from '@/components/WTitlebanner.vue'
import api from '@/utils/request'

export default {
    name: 'GenericIndexPage',
    components: {
        WTitlebanner,
    },
    data() {
        return {
            configs: [],
            selectedConfig: null
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
                })
                .catch(error => {
                    console.warn(error)
                })
        },
    },
}
</script>

<template>
    <div>
        <w-titlebanner title="Generic record entry"></w-titlebanner>

        <v-container>
            <v-autocomplete
                v-model="selectedConfig"
                :items="configs"
                item-text="name"
                item-value="id"
                label="Resource"
            ></v-autocomplete>
            
            <v-spacer></v-spacer>
            <v-btn
                v-if="selectedConfig"
                color="primary"
                elevation="2"
                :to="'/generic/' + selectedConfig"
            >
            Add dataset
            </v-btn>
        </v-container>
    </div>
</template>