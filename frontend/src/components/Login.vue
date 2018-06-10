<template>
    <div class="form-container" :class="{'is-loading': loading}">
      <span class="icon has-text-primary is-large ttitle">
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
            <button class="button is-success" type="submit">
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
          <button class="button is-warning" @click="$router.push('/signup')">
            <span class="icon">
              <i class="fas fa-user-plus"></i>
            </span>
            <span>Registrati</span>
          </button>
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
        email: this.email.value,
        password: this.password.value
      }).then(() => {
        this.loading = false
        this.$router.push('/')
      }, (resp) => {
        this.loading = false
        this.$toast.open({
          message: this.apiGetError(resp.body),
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
  .button {
    width: 100%;
    margin-top: 10px;
  }
</style>
