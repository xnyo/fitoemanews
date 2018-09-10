// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from '@/App'
import router from '@/router'
import Buefy from 'buefy'
import VueResource from 'vue-resource'
import VueRaven from 'vue-raven'

import store from '@/store'
import config from '@/config'
import ApiMixin from '@/mixins/api'

Vue.config.productionTip = false
if (config.hasOwnProperty('sentryDSN') && config.sentryDSN !== '') {
  Vue.use(VueRaven, {
    dsn: config.sentryDSN
  })
} else {
  console.warn('Raven client is disabled')
}
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
      this.$store.commit('apiOnline')
    }, () => {
      this.$store.commit('apiOffline')
    })
    this.$store.commit('setLoggingIn', true)
    this.checkLogin()
  },
  methods: {
    checkLogin () {
      this.$store.commit('setLoggingIn', true)
      let route = this.$router.resolve(window.location.pathname).route
      this.$http.get(this.apiUrl('api/v1/user'))
        .then(
          (resp) => {
            if (route.meta.hasOwnProperty('guestsOnly') && route.meta.guestsOnly) {
              this.$router.push('/')
            }
            this.$store.commit('setLoggingIn', false)
            this.$store.commit('setUserInfo', resp.body)
          }, (resp) => {
            this.$store.commit('setLoggingIn', false)
            this.$store.commit('resetUserInfo')
            if (route.meta.hasOwnProperty('protected') && route.meta.protected) {
              this.$router.push('/login')
            }
          }
        )
    }
  }
})
