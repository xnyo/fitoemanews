<template>
  <div class='medicinepicker'>
    <b-taginput
        v-model="chosenMedicines"
        :data="filteredMedicines"
        autocomplete
        placeholder="Inserisci il nome di un medicinale"
        field="latin_name"
        @typing="getMedicines">
        <template slot-scope="props">
          <div>
            <span v-html="highlightMatch(props.option.latin_name, searchQuery)"></span>
            ·
            <small v-html="highlightMatch(props.option.botanic_name, searchQuery)"></small>
            ·
            <i v-html="highlightMatch(props.option.english_name, searchQuery)"></i>
          </div>
        </template>
    </b-taginput>
  </div>
</template>

<script>
import _ from 'underscore'

export default {
  data () {
    return {
      filteredMedicines: [],
      chosenMedicines: [],
      searchQuery: ''
    }
  },
  methods: {
    getMedicines: _.debounce(function (text) {
      this.searchQuery = text
      this.$http.get(this.apiUrl('api/v1/herbs'), {
        params: {
          query: text,
          fetch_documents: false,
          limit: 5
        }
      }).then((resp) => {
        this.filteredMedicines = resp.body.herbs.filter(
          el => {
            let found = false
            this.chosenMedicines.every((chosenMedicine) => {
              if (chosenMedicine.id === el.id) {
                found = true
                return false
              }
              return true
            })
            return !found
          }
        )
      })
    }, 250),
    highlightMatch (haystack, needle) {
      let regex = new RegExp(`(${needle})`, 'gi')
      if (!needle) return haystack
      return haystack.replace(regex, '<b>$1</b>')
    }
  }
}
</script>

<style scoped>
  .medicinepicker {
    margin-top: 20px;
  }
</style>
