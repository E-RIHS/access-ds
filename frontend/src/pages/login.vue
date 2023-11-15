<script>
import WTitlebanner from '@/components/WTitlebanner.vue'

export default {
    name: 'LoginPage',
    components: {
        WTitlebanner,
    },
    data() {
        return {
            callbackRoute: this.$route.query.route
        }
    },
    methods: {
        loginWithOrcid() {
            // redirect to the login api endpoint
            window.location.href = `${import.meta.env.VITE_API_URL}/auth/login?uiroute=${this.callbackRoute}`
        }
    }
}
</script>


<template>
    <div>
        <w-titlebanner title="Login with ORCID"></w-titlebanner>
        <v-container>
            <v-alert outlined text type="info">
                <div>
                    <strong>This site uses ORCID for secure authentication. </strong><br/>
                    The first time you login, you will be asked to grant permission to this site to access your ORCID record.
                    You can revoke this permission at any time in your ORCID account settings.
                    The login process will link your personal ORCID ID and your name to your E-RIHS Metadata Collector account, but does not collect any other information about you. 
                    This site will not (and cannot) alter, add or delete anything on your ORCID profile.
                    The sole purpose is to provide a secure login mechanism for the E-RIHS website and to identify your contributions in the E-RIHS Metadata Collector. 
                    Your data is securily stored on a server managed by KIK-IRPA. You have the right to request the deletion of your account at any time.
                </div>
            </v-alert>
            
            <v-btn color="primary" @click="loginWithOrcid">Login with ORCID</v-btn>
            <br/><br/>
            callbackroute: {{ callbackRoute  }}
        </v-container>
    
    </div>
</template>
