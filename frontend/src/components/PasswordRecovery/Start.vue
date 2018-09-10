<template>
    <div v-if="!done" class="form-container" :class="{'is-loading': loading}">
      <span class="icon has-text-primary is-large ttitle">
        <i class="fas fa-unlock-alt fa-2x"></i>
        <h3 class="title">Recupero password</h3>
      </span>
      <b-message type="is-warning">
        Inserisci l'email che hai usato per registrarti per ricevere un link per reimpostare la tua password.
      </b-message>
      <section>
        <form @submit.prevent="submit">
          <b-field label="Email" :type="formData.email.type" :message="formData.email.message">
            <b-input v-model="formData.email.value" @blur="checkEmail(formData.email)"></b-input>
          </b-field>

          <div class="control">
            <button class="button is-warning" type="submit" :disabled="!isFormDataValid">
              <span class="icon">
                <i class="fas fa-key"></i>
              </span>
              <span>Invia link recupero password</span>
            </button>
          </div>
        </form>
      </section>
    </div>
    <simple-message-page
      v-else
      title="Ci siamo quasi!"
      icon="fa-key"
      colour="success"
    >
      <p>Se l'indirizzo inserito corrisponde ad un account EmaNews, verrà inviata una email contenente un link per resettare la password.</p>
    </simple-message-page>
</template>

<script>
import SimpleMessagePage from '@/components/SimpleMessagePage.vue'
import FormValidatorMixin from '@/mixins/form-validator'
import ToastMixin from '@/mixins/toast'

export default {
  data () {
    return {
      loading: false,
      done: false,
      formData: {
        email: {
          type: '',
          message: '',
          value: ''
        }
      }
    }
  },
  methods: {
    submit () {
      this.loading = true
      this.$http.post(this.apiUrl('api/v1/password_recovery'), {
        email: this.formData.email.value
      }).then((resp) => {
        this.loading = false
        this.done = true
      }, (resp) => {
        this.loading = false
        this.openApiErrorToast(resp)
      })
    }
  },
  watch: {
    'formData.email.value' () { this.checkEmail(this.formData.email) }
  },
  components: {SimpleMessagePage},
  mixins: [FormValidatorMixin, ToastMixin]
}
</script>
