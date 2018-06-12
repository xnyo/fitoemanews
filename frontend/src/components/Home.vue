<template>
  <div>
    <div class="notification" v-if="$store.getters.loggedIn">
      <b-table
        :data="data"
        paginated
        per-page="50"
        detailed
        detail-key="id"
        hoverable
      >
        <template slot-scope="props">
            <b-table-column field="id" label="Nome latino" sortable>
                {{ props.row.latin_name }}
            </b-table-column>

            <b-table-column field="botanic_name" label="Nome botanico" sortable>
                {{ props.row.botanic_name }}
            </b-table-column>

            <b-table-column field="english_name" label="Nome inglese" sortable>
                {{ props.row.english_name }}
            </b-table-column>

            <b-table-column field="status" label="Stato" class="text-centered" sortable>
              <b-tooltip :label="statusTooltipText(props.row.status)" position="is-left" type="is-dark" animated>
                <b-tag :type="statusColour(props.row.status)">{{ props.row.status }}</b-tag>
              </b-tooltip>
            </b-table-column>

            <b-table-column field="latest_update" label="Ultimo agg." class="text-centered" sortable width="110">
              {{ new Date(props.row.latest_update * 1000).toLocaleDateString() }}
            </b-table-column>

            <b-table-column field="url" label="Link" class="text-centered" width="110">
              <a :href="props.row.url" target="_blank" class="button is-small is-light">Consulta</a>
            </b-table-column>
        </template>

        <template slot="detail" slot-scope="props">
          <b-table :data="props.row.documents">
            <template slot-scope="docprops">
              <b-table-column field="type" class="text-centered" label="Tipo" sortable>
                <b-tag :type="documentTypeColour(docprops.row.type)">{{ documentType(docprops.row.type) }}</b-tag>
              </b-table-column>
              <b-table-column field="name" label="Nome" sortable>{{ docprops.row.name }}</b-table-column>
              <b-table-column field="language" label="Lingua" sortable>{{ docprops.row.language }}</b-table-column>
              <b-table-column field="first_published" label="Data pubbl." sortable>{{ new Date(docprops.row.first_published * 1000).toLocaleDateString() }}</b-table-column>
              <b-table-column field="last_updated_ema" label="Ultimo agg." sortable>{{ docprops.row.last_updated_ema }}</b-table-column>
              <b-table-column field="url" label="Link"><a :href="docprops.row.url" target="_blank" class="button is-small is-primary">Consulta</a></b-table-column>
            </template>
          </b-table>
        </template>
      </b-table>
    </div>
    <!-- <div i="main-container" class="container is-widescreen" v-else> -->
      <!-- <div class="notification"> -->
        <!-- Per favore, effettua l'accesso: -->

      <!-- </div> -->
    <!-- </div> -->
  </div>
</template>

<script>
export default {
  data () {
    return {
      data: []
    }
  },
  beforeMount () {
    this.$store.commit('setHeader', {
      subtitle: 'Homepage'
    })
  },
  mounted () {
    this.$http.get(this.apiUrl('api/v1/herbs')).then(resp => { this.data = resp.body.herbs })
  },
  methods: {
    statusTooltipText (letter) {
      switch (letter) {
        case 'R': return 'Rapporteur assigned'
        case 'C': return 'ongoing call for scientific data'
        case 'D': return 'Draft under discussion'
        case 'P': return 'Draft published'
        case 'PF': return 'Assessment close to finalisation (pre-final)'
        case 'F': return 'Final opinion adopted'
      }
    },
    statusColour (letter) {
      switch (letter) {
        case 'R': return 'is-dark'
        case 'C': return 'is-warning'
        case 'D': return 'is-primary'
        case 'P': return 'is-danger'
        case 'PF': return 'is-primary'
        case 'F': return 'is-success'
      }
    },
    documentType (type) {
      if (type === 'consultation') {
        return 'Consultation'
      }
      return 'Altro'
    },
    documentTypeColour (type) {
      console.log(type)
      if (type === 'consultation') {
        return 'is-dark-blue'
      }
      return 'is-dark'
    }
  }
}
</script>

<style scoped>
  .tag {
    text-align: center;
  }
</style>
