<template>
  <div>
    <div class="form-container wide" :class="{'is-loading': loading}">
      <div :class="{'not-visible': loading}">
        <b-message type="is-warning" has-icon v-if="latestKey !== ''">
          La tua nuova API Key è:<br><code>{{ latestKey }}</code><br>
          Custodiscila con cura, non ti sarà mostrata nuovamente e non sarà possibile recuperarla in alcun modo.
        </b-message>
        <div class="block" v-else>
          Qui hai la possibilità di creare nuove API Key per utilizzare i dati resi disponibili da EmaNews fuori da questo sito.
          Se non sei uno sviluppatore, ignora questa pagina.
        </div>
        <h6 class="title is-6 text-centered" v-if="apiKeys.length === 0">Non hai nessuna api key</h6>
        <div class="block" v-else>
          <b-table :data="apiKeys">
            <template slot-scope="props">
              <b-table-column field="name" label="Nome">
                  {{ props.row.name }}
              </b-table-column>
              <b-table-column label="Azioni" numeric>
                <a class="button is-danger is-small" @click="deleteKey(props.row.id)">
                  <span class="icon">
                    <i class="fas fa-trash"></i>
                  </span>
                </a>
              </b-table-column>
            </template>
          </b-table>
        </div>

        <div class="block text-centered">
          <button class="button is-primary" @click="isNewModalActive = true">
            <span class="icon">
              <i class="fas fa-key"></i>
            </span>
            <span>Nuova API Key</span>
          </button>
        </div>
      </div>
    </div>
    <b-modal :active.sync="isNewModalActive" has-modal-card>
      <new-key-modal @create="onCreateKey"></new-key-modal>
    </b-modal>
  </div>
</template>

<script>
import NewKeyModal from '@/components/ApiKeys/NewKeyModal.vue'
import ToastMixin from '@/mixins/toast'

export default {
  data () {
    return {
      apiKeys: [],
      isNewModalActive: false,
      loading: true,
      latestKey: ''
    }
  },
  mounted () {
    this.load()
  },
  methods: {
    load () {
      this.loading = true
      this.$http.get(this.apiUrl('api/v1/api_keys')).then((resp) => {
        this.apiKeys = resp.body
        this.loading = false
      })
    },
    onCreateKey (e) {
      this.load()
      this.latestKey = e.key
    },
    deleteKey (id) {
      this.loading = true
      this.$http.delete(this.apiUrl(`api/v1/api_keys/${id}`)).then((resp) => {
        this.latestKey = ''
        this.openSuccessToast('API Key eliminata!')
        this.load()
      }, (resp) => {
        this.openApiErrorModal(resp)
      })
    }
  },
  components: {NewKeyModal},
  mixins: [ToastMixin]
}
</script>

<style>

</style>
