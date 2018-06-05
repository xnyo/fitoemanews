<template>
    <div id="login-container" class="container" :class="{'is-loading': loading}">
      <span class="icon has-text-primary is-large">
        <i class="fas fa-sign-in-alt fa-2x"></i>
        <h3 class="title">Login</h3>
      </span>
      <section>
        <form @submit.prevent="login">
          <b-field label="Email" :type="email.type" :message="email.message">
            <b-input v-model="email.value" type="email"></b-input>
          </b-field>

          <b-field label="Password" :type="password.type" :message="password.message">
            <b-input v-model="password.value" type="password"></b-input>
          </b-field>

          <div class="control">
            <button class="button is-success" @click="login" type="submit">
              <span class="icon">
                <i class="fas fa-sign-in-alt"></i>
              </span>
              <span>Login</span>
            </button>
          </div>
        </form>
        <hr>
        <div class="text-centered">Non hai un account?</div>
        <div class="control">
          <a class="button is-warning">
            <span class="icon">
              <i class="fas fa-user-plus"></i>
            </span>
            <span>Registrati</span>
          </a>
        </div>
      </section>
    </div>
</template>

<script>
import ApiMixin from '@/mixins/api'

export default {
  data () {
    return {
      email: {
        value: '',
        type: '',
        message: ''
      },
      password: {
        value: '',
        type: '',
        message: ''
      },
      loading: false
    }
  },
  beforeMount () {
    this.$store.commit('setHeader', {
      title: 'Login',
      subtitle: 'Inserisci le tue credenziali per accedere',
      colour: 'primary'
    })
  },
  methods: {
    login () {
      let error = false
      let fields = [
        {
          field: this.email,
          readableName: 'la tua email'
        },
        {
          field: this.password,
          readableName: 'la tua password'
        }
      ]
      fields.forEach(element => {
        element.field.value = element.field.value.trim()
        if (element.field.value === '') {
          element.field.type = 'is-danger'
          element.field.message = `Per favore, inserisci ${element.readableName}`
          error = true
        } else {
          element.field.type = ''
          element.field.message = ''
        }
      })
      if (error) {
        return
      }

      this.loading = true
      this.$http.post(this.apiUrl('api/v1/login'), {
        email: this.email,
        password: this.password
      }).then(() => {
        this.loading = false
      }, (resp) => {
        let msg = 'Errore del server. Riprovare più tardi.'
        if (resp.hasOwnProperty('message')) {
          msg = resp.body.message
        }
        this.loading = false
        this.$toast.open({
          message: msg,
          type: 'is-danger',
          position: 'is-bottom',
          duration: 4000
        })
      })
    }
  },
  mixins: [ApiMixin]
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
