import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    header: {
      title: '',
      subtitle: '',
      colour: ''
    }
  },
  mutations: {
    setHeader: (state, header) => {
      state.header = header
    }
  }
})
