<template>
    <div class="form-container" :class="{'is-loading': loading}">
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
import _ from 'underscore'
import UtilsMixin from '@/mixins/utils'

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
  beforeMount () {
    this.$store.commit('setHeader', {
      title: 'Registrazione',
      subtitle: 'Inserisci i tuoi dati e crea un nuovo account'
    })
  },
  methods: {
    checkEmptyField (field) {
      field.value = field.value.trim()
      if (field.value === '') {
        field.message = 'Questo campo è obbligatorio'
        field.type = 'is-danger'
        return false
      } else {
        field.message = ''
        field.type = 'is-success'
        return true
      }
    },
    checkEmail (field) {
      if (this.checkEmptyField(field) && !this.validateEmail(field.value)) {
        field.message = 'Indirizzo email non valido'
        field.type = 'is-danger'
      }
    },
    checkPasswordStrength: _.debounce(function () {
      this.$http.get(this.apiUrl('api/v1/zxcvbn'), {
        params: {
          input: this.formData.password.value
        }
      }).then((resp) => {
        this.passwordBarValue = resp.data.strength
        this.checkPasswords()
      }, (resp) => {
        this.passwordBarValue = 0
        this.checkPasswords()
      })
    }, 500),
    checkPasswords (field) {
      if (typeof field !== 'undefined') {
        this.checkEmptyField(field)
      }
      if (this.formData.password.value === '' || this.formData.repeatPassword.value === '') {
        return
      }
      if (this.formData.password.value === this.formData.repeatPassword.value) {
        this.formData.password.type = 'is-success'
        this.formData.password.message = ''
        this.formData.repeatPassword.type = 'is-success'
        this.formData.repeatPassword.message = ''
      }

      let msg = ''
      if (this.passwordBarValue > -1 && this.passwordBarValue < 50) {
        msg = 'La password scelta è troppo debole'
      } else if (this.formData.password.value !== this.formData.repeatPassword.value) {
        msg = 'Le due password non corrispondono'
      }
      if (msg !== '') {
        this.formData.password.type = 'is-danger'
        this.formData.password.message = ''
        this.formData.repeatPassword.type = 'is-danger'
        this.formData.repeatPassword.message = msg
      }
    },
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
      ).then(resp => {
        this.loading = false
        console.log('ok')
      }, resp => {
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
  computed: {
    passwordBarColour () {
      if (this.passwordBarValue <= 25) {
        return 'is-danger'
      } else if (this.passwordBarValue > 25 && this.passwordBarValue <= 50) {
        return 'is-warning'
      } else {
        return 'is-success'
      }
    },
    isFormDataValid () {
      for (let key in this.formData) {
        if (this.formData[key].type !== 'is-success') {
          return false
        }
      }
      return true
    }
  },
  mixins: [UtilsMixin]
}
</script>

<style scoped>
  .form-container {
    width: 50% !important;
  }
  .button {
    width: 100%;
    margin-top: 10px;
  }
</style>
