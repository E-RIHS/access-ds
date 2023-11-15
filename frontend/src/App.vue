<script>
import WFooter from './components/WFooter.vue'
import WAppbar from './components/WAppbar.vue'

export default {
    name: 'App',
    components: {
		WFooter,
        WAppbar
	},
    data() {
        return {
            token: null,
        }
    },
    mounted() {
        let token = localStorage.getItem('token')
        if (token) {
            console.log('User is logged in')
            this.token = token
            // TODO: check with backend if token is valid
        } else {
            // get the current route from the url
            let route = window.location.href
            route = route.replace(import.meta.env.VITE_FRONTEND_URL, '') // remove the frontend url part
            
            // redirect to login page
            // only if not already on the login or callback pages
            if (!(route.startsWith('/login') || route.startsWith('/callback'))) {
                console.log('User is not logged in: redirecting to login page')
                // route to login page with current route as parameter
                this.$router.push({ name: 'login', query: { route: route } })
            }
        }
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
