<template>
  <div class="form-container wide">
    <div>
      <h6 class="title is-6"><i class="fas fa-bell"></i> Ricevi notifiche:</h6>
      <div class="block">
        <div class="field">
          <b-checkbox v-model="when" native-value="new_herb">
            Quando un nuovo medicinale viene inserito
          </b-checkbox>
        </div>
        <div class="field">
          <b-checkbox v-model="when" native-value="update_herb_status">
            Quando un medicinale cambia stato
          </b-checkbox>
        </div>
        <div class="field">
          <b-checkbox v-model="when" native-value="new_doc">
            Quando un nuovo documento viene inserito
          </b-checkbox>
        </div>
        <div class="field">
          <b-checkbox v-model="when" native-value="update_doc">
            Quando un documento viene aggiornato
          </b-checkbox>
        </div>
      </div>

      <hr>

      <h6 class="title is-6"><i class="fas fa-rocket"></i> Tramite:</h6>
      <div class="field">
        <b-checkbox v-model="by" native-value="Vane">
          Email
        </b-checkbox>
      </div>

      <div class="block text-centered">
        <div class="field">
          <a class="button is-small is-success">
            <span class="icon is-small">
              <i class="fas fa-paper-plane"></i>
            </span>
            <span>Collega account Telegram</span>
          </a>
        </div>
      </div>

      <hr>

      <h6 class="title is-6"><i class="fas fa-capsules"></i>  Per:</h6>
      <div class="block">
        <div class="field">
          <b-radio v-model="medicinesHowMany" native-value="all">
            Tutti i medicinali
          </b-radio>
        </div>
        <div class="field">
          <b-radio v-model="medicinesHowMany" native-value="some">
            Alcuni medicinali
          </b-radio>
          <medicine-picker v-if="medicinesHowMany === 'some'"></medicine-picker>
        </div>
      </div>

      <div class="block text-centered">
        <a class="button is-primary">
          <span class="icon is-small"><i class="fas fa-check"></i></span>
          <span>Salva impostazioni</span>
        </a>
      </div>
    </div>

  </div>
</template>

<script>
import SimpleMessagePage from '@/components/SimpleMessagePage.vue'
import MedicinePicker from '@/components/NotificationSettings/MedicinePicker.vue'

export default {
  data () {
    return {
      when: [],
      by: [],
      medicinesHowMany: ''
    }
  },
  components: {SimpleMessagePage, MedicinePicker}
}
</script>

<style>

</style>
