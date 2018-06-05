import config from '@/config'

export default {
  methods: {
    apiUrl (url) {
      return `${config.apiURL}/${url}`
    }
  }
}
