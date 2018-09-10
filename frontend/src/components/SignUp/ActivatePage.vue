<template>
  <simple-message-page
    class="centered-msg-content"
    :title="hasError ? 'Si è verificato un errore' : 'Account attivato!'"
    :icon="hasError ? 'fa-exclamation-circle' : 'fa-check-circle'"
    :colour="hasError ? 'danger' : 'success'"
    :class="{'is-loading hide-children': loading}"
  >
    <div v-if="hasError">
      <p>{{ errorMessage }}</p>
    </div>
    <div v-else>
      <p>
        Il tuo account è stato attivato!
      </p>
      <div>
        <button @click="$router.push('/login')" class="button is-primary">Vai al login</button>
      </div>
    </div>
  </simple-message-page>
</template>

<script>
import SimpleMessagePage from '@/components/SimpleMessagePage.vue'

export default {
  data () {
    return {
      loading: true,
      errorMessage: ''
    }
  },
  beforeMount () {
    this.$store.commit('setHeader', {
      title: 'Attivazione account'
    })
  },
  mounted () {
    this.$http.post(this.apiUrl(`api/v1/activate/${this.$route.params.token}`))
      .then((resp) => {
        this.loading = false
      }, (resp) => {
        this.loading = false
        this.errorMessage = this.apiGetError(resp.body)
      })
  },
  computed: {
    hasError () {
      return this.errorMessage !== ''
    }
  },
  components: {SimpleMessagePage}
}
</script>
