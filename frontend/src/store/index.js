import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const defaultUserInfo = {
  id: 0,
  name: '',
  surname: '',
  privileges: 0,
  gravatar_hash: ''
}

const store = new Vuex.Store({
  state: {
    header: {
      title: '',
      subtitle: ''
    },
    api: {
      checkingStatus: true,
      offline: false
    },
    userInfo: Object.assign({}, defaultUserInfo),
    loggingIn: true
  },
  getters: {
    loggedIn: (state) => {
      return state.userInfo.id > 0
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
    },
    setUserInfo: (state, v) => {
      // state.userInfo = Object.assign({}, state.userInfo, v)
      state.userInfo = v
    },
    resetUserInfo: (state) => {
      state.userInfo = Object.assign({}, defaultUserInfo)
    },
    setLoggingIn: (state, v) => {
      state.loggingIn = v
    }
  }
})

export default store
