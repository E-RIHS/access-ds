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
            <v-alert outlined text type="info">
                Not yet implemented
            </v-alert>
        </v-container>
    </div>
</template>