export default {
  methods: {
    openApiErrorToast (resp) {
      this.$toast.open({
        message: this.apiGetError(resp.body),
        type: 'is-danger',
        position: 'is-bottom',
        duration: 4000
      })
    },
    openSuccessToast (msg) {
      this.$toast.open({
        message: msg,
        duration: 4000,
        type: 'is-success',
        position: 'is-bottom'
      })
    }
  }
}
