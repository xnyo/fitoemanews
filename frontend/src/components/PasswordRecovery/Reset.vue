<template>
  <div v-if="!done" class="form-container" :class="{'is-loading': loading}">
    <span class="icon has-text-primary is-large ttitle">
      <i class="fas fa-unlock-alt fa-2x"></i>
      <h3 class="title">Reset password</h3>
    </span>
    <section>
      <form @submit.prevent="submit">
        <b-field label="Password" :type="formData.password.type" :message="formData.password.message">
          <b-input v-model="formData.password.value" type="password" @blur="checkPasswords(formData.password)" @input="checkPasswordStrength"></b-input>
        </b-field>

        <progress class="progress is-small" :class="[passwordBarColour]" :value="passwordBarValue" max="100">15%</progress>

        <b-field label="Ripeti password" :type="formData.repeatPassword.type" :message="formData.repeatPassword.message">
          <b-input v-model="formData.repeatPassword.value" type="password" @blur="checkPasswords(formData.repeatPassword)"></b-input>
        </b-field>

        <div class="control">
          <button class="button is-warning" type="submit" :disabled="!isFormDataValid">
            <span class="icon">
              <i class="fas fa-key"></i>
            </span>
            <span>Cambia password</span>
          </button>
        </div>
      </form>
    </section>
  </div>
  <simple-message-page
    v-else
    class="centered-msg-content"
    title="È fatta!"
    icon="fa-key"
    colour="success"
  >
    <div>
      <p>La tua password è stata reimpostata correttamente.</p>
      <div>
        <button @click="$router.push('/login')" class="button is-primary">Vai al login</button>
      </div>
    </div>
  </simple-message-page>
</template>

<script>
import SimpleMessagePage from '@/components/SimpleMessagePage.vue'
import FormValidatorMixin from '@/mixins/form-validator'
import ToastMixin from '@/mixins/toast'

export default {
  data () {
    return {
      formData: {
        password: {
          value: '',
          type: '',
          message: ''
        },
        repeatPassword: {
          value: '',
          type: '',
          message: ''
        }
      },
      passwordBarValue: 0,
      loading: true,
      done: false
    }
  },
  methods: {
    submit () {
      this.loading = true
      this.$http.post(this.apiUrl(`api/v1/password_reset/${this.$route.params.token}`), {
        password: this.formData.password.value
      }).then((resp) => {
        this.loading = false
        this.done = true
      }, (resp) => {
        this.loading = false
        this.openApiErrorToast(resp)
      })
    }
  },
  mounted () {
    this.$http.get(this.apiUrl(`api/v1/password_reset/${this.$route.params.token}`)).then(() => {
      this.loading = false
    }, (resp) => {
      this.openApiErrorToast(resp)
      this.$router.push('/login')
    })
  },
  computed: {
    passwordBarColour () { return this.passwordStrengthClass(this.passwordBarValue) }
  },
  watch: {
    'formData.password.value' () { this.checkPasswords(this.formData.password) },
    'formData.repeatPassword.value' () { this.checkPasswords(this.formData.repeatPassword) }
  },
  components: {SimpleMessagePage},
  mixins: [FormValidatorMixin, ToastMixin]
}
</script>

<style>

</style>
