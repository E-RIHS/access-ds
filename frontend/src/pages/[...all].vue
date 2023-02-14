<script>
import WTitlebanner from '@/components/WTitlebanner.vue'

export default {
    name: 'ErrorPage',
    components: {
        WTitlebanner,
    },
}
</script>

<template>
    <div>
        <w-titlebanner title="Page not found"></w-titlebanner>

        <v-container>
            <v-alert outlined text type="error">
                404 Not Found
            </v-alert>
        </v-container>
    </div>
</template>
