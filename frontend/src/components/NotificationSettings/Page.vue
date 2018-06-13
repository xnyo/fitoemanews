<template>
  <div class="form-container wide">
    <div>
      <h6 class="title is-6"><i class="fas fa-bell"></i> Ricevi notifiche:</h6>
      <div class="block">
        <div class="field">
          <b-checkbox v-model="when" native-value="NEW_MEDICINE">
            Quando un nuovo medicinale viene inserito
          </b-checkbox>
        </div>
        <div class="field">
          <b-checkbox v-model="when" native-value="MEDICINE_UPDATE">
            Quando un medicinale cambia stato
          </b-checkbox>
        </div>
        <div class="field">
          <b-checkbox v-model="when" native-value="NEW_DOCUMENT">
            Quando un nuovo documento viene inserito
          </b-checkbox>
        </div>
        <div class="field">
          <b-checkbox v-model="when" native-value="DOCUMENT_UPDATE">
            Quando un documento viene aggiornato
          </b-checkbox>
        </div>
      </div>

      <hr>

      <h6 class="title is-6"><i class="fas fa-rocket"></i> Tramite:</h6>
      <div class="field">
        <b-checkbox v-model="by" native-value="EMAIL">
          Email
        </b-checkbox>
      </div>
      <div class="field" v-if="telegramLinked">
        <b-checkbox v-model="by" native-value="TELEGRAM">
          <span>
            Telegram
          </span>
        </b-checkbox>
      </div>
      <div class="block text-centered">
        <div class="field">
          <button
            class="button is-small"
            :class="{'is-success': !telegramLinked, 'is-danger': telegramLinked}"
            @click="onLinkUnlinkTelegramButtonClick"
          >
            <span class="icon is-small">
              <i class="fas" :class="{'fa-paper-plane': !telegramLinked, 'fa-unlink': telegramLinked}"></i>
            </span>
            <span>{{ telegramLinked ? 'Scollega' : 'Collega' }} account Telegram</span>
          </button>
        </div>
      </div>

      <hr>

      <h6 class="title is-6"><i class="fas fa-capsules"></i>  Per:</h6>
      <div class="block">
        <div class="field">
          <b-radio v-model="allHerbs" :native-value="true">
            Tutti i medicinali
          </b-radio>
        </div>
        <div class="field">
          <b-radio v-model="allHerbs" :native-value="false">
            Alcuni medicinali
          </b-radio>
          <medicine-picker v-model="herbs" :initial-value="herbs" v-if="!allHerbs"></medicine-picker>
        </div>
      </div>

      <div class="block text-centered">
        <button class="button is-primary" @click="save">
          <span class="icon is-small"><i class="fas fa-check"></i></span>
          <span>Salva impostazioni</span>
        </button>
      </div>
    </div>

    <b-modal :active.sync="isTelegramLinkModalActive" @close="load" has-modal-card>
      <telegram-link-form></telegram-link-form>
    </b-modal>

  </div>
</template>

<script>
import SimpleMessagePage from '@/components/SimpleMessagePage.vue'
import MedicinePicker from '@/components/NotificationSettings/MedicinePicker.vue'
import TelegramLinkForm from '@/components/NotificationSettings/TelegramLinkForm.vue'
import ToastMixin from '@/mixins/toast'

export default {
  data () {
    return {
      when: [],
      by: [],
      herbs: [],
      allHerbs: true,
      loading: true,
      telegramLinked: false,
      isTelegramLinkModalActive: false
    }
  },
  mounted () {
    this.load()
  },
  methods: {
    load () {
      this.loading = true
      this.$http.get(this.apiUrl('api/v1/notification_settings')).then((resp) => {
        this.loading = false
        this.when = resp.body.when
        this.by = resp.body.by
        this.allHerbs = !(resp.body.herbs instanceof Array)
        this.herbs = !this.allHerbs ? resp.body.herbs : []
        this.telegramLinked = resp.body.telegram_linked
      })
    },
    save () {
      this.loading = true
      this.$http.post(this.apiUrl('api/v1/notification_settings'), {
        when: this.when,
        by: this.by,
        herbs: this.allHerbs ? true : this.herbs.map(el => el.id)
      }).then((resp) => {
        this.loading = false
        this.openSuccessToast('Impostazioni salvate correttamente!')
        this.load()
      }, (resp) => {
        this.loading = false
        this.openApiErrorToast(resp)
      })
    },
    onLinkUnlinkTelegramButtonClick () {
      if (!this.telegramLinked) {
        this.isTelegramLinkModalActive = true
      } else {
        this.loading = true
        this.$http.delete(this.apiUrl('api/v1/telegram')).then((resp) => {
          this.openSuccessToast('Account telegram scollegato con successo!')
          this.load()
        }, (resp) => {
          this.openApiErrorToast(resp)
        })
      }
    }
  },
  components: {SimpleMessagePage, MedicinePicker, TelegramLinkForm},
  mixins: [ToastMixin]
}
</script>

<style>

</style>
