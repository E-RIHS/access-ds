<script>
export default {
    name: 'CallbackPage',
    data() {
        return {
            token: this.$route.query.token,
            name: this.$route.query.name,
            orcid: this.$route.query.orcid,
            callbackRoute: this.$route.query.route
        }
    },
    mounted() {
        this.storeToken()
    },
    methods: {
        storeToken() {
            console.log('Storing token and user info')
            // store token in local storage
            localStorage.setItem('token', this.token)
            // store name and orcid in session storage
            sessionStorage.setItem('name', this.name)
            sessionStorage.setItem('orcid', this.orcid)
            // full redirect to the callback route
            // no router push, to make sure all components are reloaded
            let url = import.meta.env.VITE_FRONTEND_URL + this.callbackRoute
            console.log('Redirecting to: ' + url)
            window.location.replace(url);
        }
    }
}
</script>


<template>

</template>