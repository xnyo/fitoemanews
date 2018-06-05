<template>
  <div id="app">
    <main-header
      :colour='$store.state.header.colour'
      :title='$store.state.header.title'
      :subtitle='$store.state.header.subtitle'
    ></main-header>
    <router-view/>
  </div>
</template>

<script>
import MainHeader from './components/MainHeader.vue'
export default {
  components: {
    MainHeader
  }
}
</script>
