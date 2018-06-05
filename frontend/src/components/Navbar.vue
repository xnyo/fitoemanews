<template>
  <nav class="navbar is-dark-blue" role="navigation" aria-label="dropdown navigation">
    <div class="navbar-start">
      <b class="navbar-item" href="https://bulma.io/">
        EmaNews
      </b>
      <a class="navbar-item" @click="$router.push('/')">
        Home
      </a>
    </div>

    <div class="navbar-end">
      <div class="navbar-item has-dropdown is-hoverable" v-if="$store.state.loggedIn">
        <a class="navbar-link">
          Utente
        </a>

        <div class="navbar-dropdown is-right">
          <a class="navbar-item">
            <span class="icon has-white-text">
              <i class="fas fa-sign-in-alt"></i>
            </span>
            <span>Login</span>
          </a>
          <a class="navbar-item">
            API Key
          </a>
          <hr class="navbar-divider">
          <div class="navbar-item">
            Logout
          </div>
        </div>
      </div>
      <a class="navbar-item" @click="$router.push('/login')" v-else>
        <span class="icon has-white-text">
          <i class="fas fa-sign-in-alt"></i>
        </span>
        <span>Login</span>
      </a>
    </div>

  </nav>
</template>

<script>
export default {
}
</script>

<style>

</style>
