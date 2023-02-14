import Vue from 'vue'
import Router from 'vue-router'
import routes from '~pages'


Vue.use(Router)

// fix: the :all route must be the last item in routes
let index = routes.findIndex(x => x.name === 'all')
routes.push(routes.splice(index, 1)[0])

export default new Router({
  mode: 'history',
  routes,
})