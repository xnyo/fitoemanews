<template>
  <div class="form-container wide">
    <div>
      <div class="block">
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
              <a class="button is-danger is-small">
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

      <b-modal :active.sync="isNewModalActive" has-modal-card>
        <new-key-modal></new-key-modal>
      </b-modal>

    </div>
  </div>
</template>

<script>
import NewKeyModal from '@/components/ApiKeys/NewKeyModal.vue'

export default {
  data () {
    return {
      apiKeys: [],
      isNewModalActive: false
    }
  },
  components: {NewKeyModal}
}
</script>

<style>

</style>
