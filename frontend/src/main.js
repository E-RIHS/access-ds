import Vue from 'vue'
import App from './App.vue'
import '@/assets/styles/index.scss'

import vuetify from './plugins/vuetify'
import router from './plugins/router'

const app = new Vue({
    router,
    vuetify,
    render: (h) => h(App),
})
app.$mount('#app')
