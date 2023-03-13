<script>
import WTitlebanner from '@/components/WTitlebanner.vue'

export default {
    name: 'SchemaConfigDetailPage',
    components: {
        WTitlebanner,
    },
}
</script>

<template>
    <div>
        <w-titlebanner :title="this.$route.params.id"></w-titlebanner>

        <v-container>
            top
        </v-container>

        <v-container fluid>
            <v-row>
                <v-col>
                    <v-card>
                        <v-card-title>
                            <v-tabs 
                                v-model="tab" 
                                v-if="!dataEntry"
                                grow>
                                <v-tab>JSON Schema</v-tab>
                                <v-tab>UI Schema</v-tab>
                                <v-tab>I18n Schema</v-tab>
                                <v-tab>Default dataset</v-tab>
                            </v-tabs>
                        </v-card-title>
                        <v-card-text v-if="tab === 0">
                        </v-card-text>
                    </v-card>
                </v-col>
                <v-col>
                    <v-card>
                        <v-card-title>
                                <v-tabs 
                                v-model="tab" 
                                v-if="!dataEntry"
                                grow>
                                <v-tab>Example form</v-tab>
                                <v-tab>Example dataset</v-tab>
                            </v-tabs>
                        </v-card-title>
                        <v-card-text v-if="tab === 0">
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>