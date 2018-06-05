import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    header: {
      title: '',
      subtitle: '',
      colour: ''
    },
    api: {
      checkingStatus: true,
      offline: false
    }
  },
  mutations: {
    setHeader: (state, header) => {
      state.header = header
    },
    apiOffline: (state) => {
      state.api.checkingStatus = false
      state.api.offline = true
    },
    apiOnline: (state) => {
      state.api.checkingStatus = false
      state.api.offline = false
    }
  }
})
