<template>
    <div class="form-container wide" :class="{'is-loading': loading}">
      <span class="icon has-text-primary is-large ttitle">
        <i class="fas fa-user-plus fa-2x"></i>
        <h3 class="title">Registrazione</h3>
      </span>
      <section>
        <form @submit.prevent="submit">
          <b-field label="Nome" :type="formData.name.type" :message="formData.name.message">
            <b-input v-model="formData.name.value" @blur="checkEmptyField(formData.name)"></b-input>
          </b-field>

          <b-field label="Cognome" :type="formData.surname.type" :message="formData.surname.message">
            <b-input v-model="formData.surname.value" @blur="checkEmptyField(formData.surname)"></b-input>
          </b-field>

          <b-field label="Email" :type="formData.email.type" :message="formData.email.message">
            <b-input v-model="formData.email.value" @blur="checkEmail(formData.email)"></b-input>
          </b-field>

          <b-field label="Password" :type="formData.password.type" :message="formData.password.message">
            <b-input v-model="formData.password.value" type="password" @blur="checkPasswords(formData.password)" @input="checkPasswordStrength"></b-input>
          </b-field>

          <progress class="progress is-small" :class="[passwordBarColour]" :value="passwordBarValue" max="100">15%</progress>

          <b-field label="Ripeti password" :type="formData.repeatPassword.type" :message="formData.repeatPassword.message">
            <b-input v-model="formData.repeatPassword.value" type="password" @blur="checkPasswords(formData.repeatPassword)"></b-input>
          </b-field>

          <!-- <div class="field">
              <b-checkbox v-model="checkboxCustom"
                  true-value="Yes"
                  false-value="No">
                  ???
              </b-checkbox>
          </div> -->

          <div class="control">
            <button class="button is-success" type="submit" :disabled="!isFormDataValid">
              <span class="icon">
                <i class="fas fa-user-plus"></i>
              </span>
              <span>Registrati</span>
            </button>
          </div>
        </form>
      </section>
    </div>
</template>

<script>
import UtilsMixin from '@/mixins/utils'
import ToastMixin from '@/mixins/toast'
import FormValidatorMixin from '@/mixins/form-validator'

export default {
  data () {
    return {
      formData: {
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
        repeatPassword: {
          value: '',
          type: '',
          message: '',
          exclude: true
        },
        name: {
          value: '',
          type: '',
          message: ''
        },
        surname: {
          value: '',
          type: '',
          message: ''
        }
      },
      passwordBarValue: 0,
      loading: false
    }
  },
  methods: {
    submit () {
      this.loading = true
      this.$http.post(
        this.apiUrl('api/v1/user'),
        Object.keys(this.formData).filter(key =>
          !this.formData[key].hasOwnProperty('exclude') || !this.formData[key].exclude
        ).reduce((obj, key) => {
          obj[key] = this.formData[key].value
          return obj
        }, {})
      ).then((resp) => {
        this.loading = false
        this.$emit('done')
      }, (resp) => {
        this.loading = false
        this.openApiErrorToast(resp)
      })
    }
  },
  computed: {
    passwordBarColour () {
      if (this.passwordBarValue <= 25) {
        return 'is-danger'
      } else if (this.passwordBarValue > 25 && this.passwordBarValue <= 50) {
        return 'is-warning'
      } else {
        return 'is-success'
      }
    }
  },
  watch: {
    'formData.name.value' () { this.checkEmptyField(this.formData.name) },
    'formData.surname.value' () { this.checkEmptyField(this.formData.surname) },
    'formData.email.value' () { this.checkEmail(this.formData.email) },
    'formData.password.value' () { this.checkPasswords(this.formData.password) },
    'formData.repeatPassword.value' () { this.checkPasswords(this.formData.repeatPassword) }
  },
  mixins: [UtilsMixin, ToastMixin, FormValidatorMixin]
}
</script>

<style scoped>
  .button {
    width: 100%;
    margin-top: 10px;
  }
</style>
