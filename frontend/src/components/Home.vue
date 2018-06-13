<template>
  <div>
    <div class="notification" v-if="$store.getters.loggedIn">
      <nav class="level">
        <div class="level-left"></div>
        <div class="level-right">
          <b-field>
            <div class="level-item">
              <b-input
                placeholder="Ricerca"
                type="search"
                icon-pack="fas"
                icon="search"
                rounded
                @input="search"
                v-model="query"
              >
              </b-input>
            </div>
          </b-field>
        </div>
      </nav>
      <b-table
        id="herbs-table"
        :data="data"

        paginated
        backend-pagination
        :total="totalHerbs"
        :per-page="perPage"
        @page-change="onPageChange"

        backend-sorting
        default-sort-direction="desc"
        :default-sort="[sortField, sortOrder]"
        @sort="onSort"

        detailed
        detail-key="id"
        hoverable
        :loading="loading"
      >
        <template slot-scope="props">
            <b-table-column field="latin_name" label="Nome latino" sortable>
                {{ props.row.latin_name }}
            </b-table-column>

            <b-table-column field="botanic_name" label="Nome botanico" sortable>
                {{ props.row.botanic_name }}
            </b-table-column>

            <b-table-column field="english_name" label="Nome inglese" sortable>
                {{ props.row.english_name }}
            </b-table-column>

            <b-table-column field="status" label="Stato" class="text-centered" sortable :custom-sort="sortStatus">
              <b-tooltip :label="statusTooltipText(props.row.status)" position="is-left" type="is-dark" animated>
                <b-tag :type="statusColour(props.row.status)">{{ props.row.status }}</b-tag>
              </b-tooltip>
            </b-table-column>

            <b-table-column field="latest_update" label="Ultimo agg." class="text-centered" sortable width="110">
              {{ formatDate(props.row.latest_update) }}
            </b-table-column>

            <b-table-column field="url" label="Link" class="text-centered" width="110">
              <a :href="props.row.url" target="_blank" class="button is-rounded is-small is-light">Consulta</a>
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
              <b-table-column field="first_published" label="Data pubbl." sortable>
                {{ formatDate(docprops.row.first_published) }}
              </b-table-column>
              <b-table-column field="last_updated_ema" label="Ultimo agg." sortable>{{ formatDate(docprops.row.last_updated_ema) }}</b-table-column>
              <b-table-column field="url" label="Link"><a :href="docprops.row.url" target="_blank" class="button is-rounded is-small is-primary">Consulta</a></b-table-column>
            </template>
          </b-table>
        </template>
      </b-table>
    </div>
  </div>
</template>

<script>
import _ from 'underscore'

export default {
  data () {
    return {
      data: [],
      loading: true,
      query: '',
      totalHerbs: 0,
      page: 1,
      perPage: 50,
      sortField: 'latin_name',
      sortOrder: 'asc'
    }
  },
  mounted () {
    this.getHerbs()
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
      if (type === 'consultation') {
        return 'is-dark-blue'
      }
      return 'is-dark'
    },

    sortStatus (a, b, isAsc) {
      const order = ['R', 'C', 'D', 'P', 'PF', 'F']
      if (order.indexOf(a.status) > order.indexOf(b.status)) {
        return isAsc ? 1 : -1
      }
      if (order.indexOf(a.status) < order.indexOf(b.status)) {
        return isAsc ? -1 : 1
      }
      return 0
    },

    formatDate (unix) {
      if (unix === null) {
        return ''
      }

      let d = new Date(unix * 1000)
      let month = String(d.getMonth() + 1)
      let day = String(d.getDate())
      const year = String(d.getFullYear())

      if (month.length < 2) month = '0' + month
      if (day.length < 2) day = '0' + day

      return `${day}/${month}/${year}`
    },

    getHerbs () {
      this.loading = true
      this.$http.get(this.apiUrl('api/v1/herbs'), {
        params: {
          query: this.query,
          limit: this.perPage,
          page: this.page - 1,
          order_by: this.sortField,
          direction: this.sortOrder
        }
      }).then((resp) => {
        this.loading = false
        this.data = resp.body.herbs
        this.totalHerbs = resp.body.total
      })
    },

    search: _.debounce(function () { this.getHerbs() }, 500),

    onPageChange (page) {
      this.page = page
      this.getHerbs()
    },

    onSort (field, order) {
      this.sortField = field
      console.log(this.sortOrder)
      this.sortOrder = order
      this.getHerbs()
    }
  }
}
</script>

<style scoped>
  .tag {
    text-align: center;
  }
</style>
