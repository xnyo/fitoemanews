// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from '@/App'
import router from '@/router'
import Buefy from 'buefy'
import 'buefy/lib/buefy.css'
import VueResource from 'vue-resource'

import store from '@/store'
import ApiMixin from '@/mixins/api'

Vue.config.productionTip = false
Vue.use(Buefy, {
  defaultIconPack: 'fas'
})
Vue.use(VueResource)
Vue.prototype.$store = store
Vue.mixin(ApiMixin)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
  mounted () {
    this.$http.get(this.apiUrl('api/v1/ping')).then(() => {
      console.log('Api online')
      this.$store.commit('apiOnline')
    }, () => {
      this.$store.commit('apiOffline')
    })
    this.$store.commit('setLoggingIn', true)
    this.checkLogin()
  },
  methods: {
    checkLogin () {
      console.log('checking login')
      this.$store.commit('setLoggingIn', true)
      let route = this.$router.resolve(window.location.pathname).route
      console.log(route)
      this.$http.get(this.apiUrl('api/v1/user'))
        .then(
          (resp) => {
            console.log('logged in')
            if (route.meta.hasOwnProperty('guestsOnly') && route.meta.guestsOnly) {
              console.log('logged in, but in guest only route. going to /.')
              this.$router.push('/')
            }
            this.$store.commit('setLoggingIn', false)
            this.$store.commit('setUserInfo', resp.body)
          }, (resp) => {
            console.log('not logged in')
            console.log(route.meta.hasOwnProperty('protected'))
            console.log(route.meta.protected)
            this.$store.commit('setLoggingIn', false)
            this.$store.commit('resetUserInfo')
            if (route.meta.hasOwnProperty('protected') && route.meta.protected) {
              console.log('logged in, but in protected route. going to /login.')
              this.$router.push('/login')
            }
          }
        )
    }
  }
})
