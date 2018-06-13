<template>
  <nav class="navbar is-dark-blue" role="navigation" aria-label="dropdown navigation">
    <div class="navbar-start">
      <b class="navbar-item">
        EmaNews
      </b>
      <a class="navbar-item" @click="$router.push('/')">
        Home
      </a>
    </div>

    <div class="navbar-end" v-if="!$store.state.loggingIn">
      <div class="navbar-item has-dropdown is-hoverable" v-if="$store.getters.loggedIn">
        <a class="navbar-link">
          <img :src="gravatarUrl" class="avatar">
          <span>
            {{ $store.state.userInfo.name }} {{ $store.state.userInfo.surname }}
          </span>
        </a>

        <div class="navbar-dropdown is-right">
          <a class="navbar-item" @click="$router.push('/notification_settings')">
            <span class="icon has-white-text">
              <i class="fas fa-bell"></i>
            </span>
            <span>Impost. notifiche</span>
          </a>
          <a class="navbar-item">
            <span class="icon has-white-text">
              <i class="fas fa-key"></i>
            </span>
            <span>API Key</span>
          </a>
          <hr class="navbar-divider">
          <a class="navbar-item" @click="logout">
            <span class="icon has-white-text">
              <i class="fas fa-sign-out-alt"></i>
            </span>
            <span>Logout</span>
          </a>
        </div>
      </div>
      <a class="navbar-item" @click="$router.push('/login')" v-else>
        <span class="icon has-white-text">
          <i class="fas fa-sign-in-alt"></i>
        </span>
        <span>Login</span>
      </a>
    </div>
    <div v-else class="navbar-end">
      <div class="navbar-item">
        <i class="fas fa-circle-notch fa-spin"></i>
      </div>
    </div>

  </nav>
</template>

<script>
export default {
  computed: {
    gravatarUrl () {
      return this.$store.getters.loggedIn ? 'https://gravatar.com/avatar/' + this.$store.state.userInfo['gravatar_hash'] : '#'
    }
  },
  methods: {
    logout () {
      this.$store.commit('setLoggingIn', true)
      this.$http.post(this.apiUrl('api/v1/logout'))
        .then(
          () => {
            window.location.replace('/login')
          },
          (resp) => {
            this.$store.commit('setLoggingIn', false)
            this.$toast.open({
              message: this.apiGetError(resp.body),
              type: 'is-danger',
              position: 'is-bottom',
              duration: 4000
            })
          })
    }
  }
}
</script>

<style>

</style>
