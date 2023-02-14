<script>
import WFooter from './components/WFooter.vue'
import WAppbar from './components/WAppbar.vue'

export default {
    name: 'App',
    components: {
		WFooter,
        WAppbar
	},
}
</script>

<template>
    <v-app id="app">
        <w-appbar></w-appbar>
        <router-view />
        <v-container fill-height></v-container> <!-- fills remaining horizontal space, if necessary -->
        <w-footer></w-footer>
    </v-app>
</template>
