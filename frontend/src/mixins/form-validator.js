import _ from 'underscore'

export default {
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
      // if (this.passwordBarValue === -1) {
      // field.type = ''
      // field.message = ''
      // return
      // }
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
    }
  },
  computed: {
    isFormDataValid () {
      for (let key in this.formData) {
        if (this.formData[key].type !== 'is-success') {
          return false
        }
      }
      return true
    }
  }
}
