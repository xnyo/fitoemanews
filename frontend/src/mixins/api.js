import config from '@/config'

export default {
  methods: {
    apiUrl (url) {
      return `${config.apiURL}/${url}`
    },
    apiGetError (data, default_) {
      let msg = 'Errore del server. Riprovare più tardi.'
      if (typeof default_ !== 'undefined') {
        msg = default_
      }
      if (data.hasOwnProperty('message')) {
        msg = data.message
      }
      return msg
    }
  }
}
