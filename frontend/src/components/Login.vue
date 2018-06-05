<template>
    <div id="login-container" class="container">
      <span class="icon has-text-primary is-large">
        <i class="fas fa-sign-in-alt fa-2x"></i>
        <h3 class="title">Login</h3>
      </span>
      <section>
        <b-field label="Email">
          <b-input v-model="email" type="email"></b-input>
        </b-field>

        <b-field label="Password">
          <b-input v-model="password" type="password"></b-input>
        </b-field>

        <a class="button is-success">
          <span class="icon">
            <i class="fas fa-sign-in-alt"></i>
          </span>
          <span>Login</span>
        </a>
        <hr>
        <div class="text-centered">Non hai un account?</div>
        <a class="button is-warning">
          <span class="icon">
            <i class="fas fa-user-plus"></i>
          </span>
          <span>Registrati</span>
        </a>
      </section>
    </div>
</template>

<script>
export default {
  data () {
    return {
      email: '',
      password: ''
    }
  },
  beforeMount () {
    this.$store.commit('setHeader', {
      title: 'Login',
      subtitle: 'Inserisci le tue credenziali per accedere',
      colour: 'primary'
    })
  }
}
</script>

<style scoped>
  #login-container {
    width: 30%;
    padding: 50px;
    margin-top: 50px;
    border-radius: 5px;
    background-color: #fff;
    box-shadow: 0 2px 3px rgba(10,10,10,.1),0 0 0 1px rgba(10,10,10,.1);
    color: #4a4a4a;
  }

  #login-container>span:first-child {
    text-align: center;
    width: 100%;
  }

  #login-container>span:first-child>i.fas {
    margin: 10px;
  }

  .button {
    width: 100%;
    margin-top: 10px;
  }
</style>


<style lang="scss" scoped>
  // @import "~bulma";

  // input {
  //   @extend .is-primary;
  // }
</style>

