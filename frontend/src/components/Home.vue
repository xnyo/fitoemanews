<template>
  <div>
    <div id="main-container" class="container is-widescreen">
      <div class="notification ">
        Homepage
      </div>
    </div>
  </div>
</template>

<script>
export default {
  beforeMount () {
    this.$store.commit('setHeader', {
      subtitle: 'Homepage'
    })
    this.$store.commit('setLoggingIn', true)
    this.$http.get(this.apiUrl('api/v1/user')).then((resp) => {
      this.$store.commit('setLoggingIn', false)
      this.$store.commit('setUserInfo', resp.body)
    }, (resp) => {
      this.$store.commit('setLoggingIn', false)
      this.$store.commit('resetUserInfo')
    })
  }
}
</script>
