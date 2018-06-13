<template>
  <form @submit.prevent="submit">
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Nuova API Key</p>
      </header>
      <section class="modal-card-body">
        <div :class="{'is-loading': loading}">
          <div :class="{'not-visible': loading}">
            <section>
              <b-field label="Nome" :type="formData.name.type" :message="formData.name.message">
                <b-input ref="input" v-model="formData.name.value" @blur="checkEmptyField(formData.name)" placeholder="Un nome che identifica la tua API Key"></b-input>
              </b-field>
            </section>
          </div>
        </div>
      </section>
      <footer class="modal-card-foot">
        <nav class="level">
          <div class="level-left">
            <div class="level-item">
              <button class="button" type="button" @click="$parent.close()">Chiudi</button>
            </div>
          </div>
          <div class="level-right">
            <div class="level-item">
              <button class="button is-primary" type="submit" :disabled="!isFormDataValid || loading">
                <span class="icon">
                  <i class="fas fa-plus"></i>
                </span>
                <span>Crea</span>
              </button>
            </div>
          </div>
        </nav>
      </footer>
    </div>
  </form>
</template>

<script>
import FormValidatorMixin from '@/mixins/form-validator'
import ToastMixin from '@/mixins/toast'

export default {
  data () {
    return {
      formData: {
        name: {
          type: '',
          message: '',
          value: ''
        }
      },
      loading: false
    }
  },
  mounted () {
    this.$refs.input.$el.children[0].focus()
  },
  methods: {
    submit () {
      if (!this.isFormDataValid) {
        return
      }

      this.loading = true
      this.$http.post(this.apiUrl('api/v1/api_keys'), {
        name: this.formData.name.value
      }).then((resp) => {
        this.openSuccessToast('API Key creata!')
        this.$parent.close()
        this.$emit('create', {
          key: resp.body.key
        })
      }, (resp) => {
        this.loading = false
        this.openApiErrorToast(resp)
      })
    }
  },
  watch: {
    'formData.name.value' () { this.checkEmptyField(this.formData.name) }
  },
  mixins: [FormValidatorMixin, ToastMixin]
}
</script>

<style scoped>
  .level {
    width: 100%;
  }

  .modal-card-body {
    overflow: hidden;
  }
</style>
