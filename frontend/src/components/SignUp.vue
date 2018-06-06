<template>
    <div class="form-container">
      <span class="icon has-text-primary is-large ttitle">
        <i class="fas fa-user-plus fa-2x"></i>
        <h3 class="title">Registrazione</h3>
      </span>
      <section>
        <form @submit.prevent="login">
          <b-field label="Nome" :type="name.type" :message="name.message">
            <b-input v-model="name.value" @blur="updateField(name)"></b-input>
          </b-field>

          <b-field label="Cognome" :type="surname.type" :message="surname.message">
            <b-input v-model="surname.value" @blur="updateField(surname)"></b-input>
          </b-field>

          <b-field label="Email" :type="email.type" :message="email.message">
            <b-input v-model="email.value" type="email" @blur="updateField(email)"></b-input>
          </b-field>

          <b-field label="Password" :type="password.type" :message="password.message">
            <b-input v-model="password.value" type="password" @blur="updateField(password)"></b-input>
          </b-field>

          <progress class="progress is-small" :class="[passwordBarColour]" :value="passwordBarValue" max="100">15%</progress>

          <b-field label="Ripeti password" :type="repeatPassword.type" :message="repeatPassword.message">
            <b-input v-model="repeatPassword.value" type="password" @blur="updateField(repeatPassword)"></b-input>
          </b-field>

          <!-- <div class="field">
              <b-checkbox v-model="checkboxCustom"
                  true-value="Yes"
                  false-value="No">
                  ???
              </b-checkbox>
          </div> -->

          <div class="control">
            <button class="button is-success" @click="" type="submit">
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


export default {
  data() {
    return {
      email: {
        value: '',
        type: '',
        message: ''
      }, password: {
        value: '',
        type: '',
        message: ''
      }, repeatPassword: {
        value: '',
        type: '',
        message: ''
      }, name: {
        value: '',
        type: '',
        message: ''
      }, surname: {
        value: '',
        type: '',
        message: ''
      },
      passwordBarValue: 70
    }
  },
  beforeMount() {
    this.$store.commit('setHeader', {
      title: 'Registrazione',
      subtitle: 'Inserisci i tuoi dati e crea un nuovo account'
    })
  },
  methods: {
    updateField (field) {
      field.value = field.value.trim()
      if (field.value === '') {
        field.message = 'Questo campo è obbligatorio'
        field.type = 'is-danger'
      } else {
        field.message = ''
        field.type = ''
      }
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
  }
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
