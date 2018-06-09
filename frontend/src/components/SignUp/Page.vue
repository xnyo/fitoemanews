<template>
    <div>
      <simple-message-page
        title="Registrazione effettuata"
        colour="success"
        icon="fa-check-circle"
        v-if="done"
      >
        La registrazione è avvenuta con successo! Per favore, clicca sul link che hai ricevuto sulla tua casella di posta elettronica per attivare il tuo account.
        Non dimenticare di controllare la cartella dello spam.
      </simple-message-page>
      <sign-up-form @done="done = true" v-else></sign-up-form>
    </div>
</template>

<script>
import SignUpForm from '@/components/SignUp/Form.vue'
import SimpleMessagePage from '@/components/SimpleMessagePage.vue'

export default {
  data () {
    return {
      done: false
    }
  },
  components: {SignUpForm, SimpleMessagePage}
}
</script>
