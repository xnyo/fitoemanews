<template>
  <div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Collega account telegram</p>
      </header>
      <section class="modal-card-body text-centered">
        <div :class="{'is-loading': loading}">
          <div :class="{'not-visible': loading}">
            <div v-if="!done">
              <p>
                Scannerizza questo QR code con il tuo smartphone per collegare il tuo account EmaNews con il tuo account Telegram e ricevere le notifiche dal nostro bot.
              </p>
              <v-lazy-image
                id='qr'
                :src="qrImage"
                src-placeholder="https://qrpi.nyodev.xyz/?data=YW1pIGkgbG92ZSB5b3UgPDM"
              ></v-lazy-image>
              <p>Se non hai la possibilità di scannerizzare il QR code ed hai Telegram installato su questo dispositivo, puoi collegare il tuo account cliccando sul pulsante in basso:</p>
              <div class="text-centered">
                <a target="_blank" :href="telegramLink" class="button is-small is-primary">
                  <span class="icon is-small">
                    <i class="fas fa-link"></i>
                  </span>
                  <span>Collega a Telegram</span>
                </a>
              </div>
              <p><b>Una volta collegato il tuo account, questa finestra si aggiornerà da sola.</b></p>
            </div>
            <div class="title is-4" v-else>
              <i class="fas fa-check-circle has-text-success"></i>
              Il tuo account è stato collegato a Telegram con successo!
            </div>
          </div>
        </div>
      </section>
      <footer class="modal-card-foot">
        <button class="button" type="button" @click="$parent.close()">Chiudi</button>
      </footer>
    </div>
  </div>
</template>

<script>
import ToastMixin from '@/mixins/toast'
import VLazyImage from 'v-lazy-image'

export default {
  data () {
    return {
      loading: true,
      done: false,
      telegramLink: '',
      interval: null
    }
  },
  mounted () {
    this.interval = setInterval(this.apiCall, 4000)
    this.apiCall()
  },
  destroyed () {
    if (this.interval !== null) {
      clearInterval(this.interval)
    }
  },
  methods: {
    apiCall () {
      this.$http.get(this.apiUrl('api/v1/telegram')).then((resp) => {
        this.loading = false
        this.telegramLink = resp.body.telegram_link
      }, (resp) => {
        if (resp.status === 406) {
          this.loading = false
          this.done = true
        } else {
          this.openApiErrorToast(resp)
        }
      })
    }
  },
  computed: {
    qrImage () { return `https://qrpi.nyodev.xyz/?data=${this.telegramLink}` }
  },
  components: {VLazyImage},
  mixins: [ToastMixin]
}
</script>

<style scoped>
  #qr {
    margin: 0 auto;
    display: block;
    height: 200px;
  }

  #qr.v-lazy-image {
    filter: blur(20px);
    transition: filter 0.7s;
  }
  #qr.v-lazy-image-loaded {
    filter: blur(0);
  }

  .button.is-small {
    margin: 10px;
  }
</style>
