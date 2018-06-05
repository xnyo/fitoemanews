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
  }
})
