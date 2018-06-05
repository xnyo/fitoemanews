<template>
  <div id="app">
    <main-header
      :colour='$store.state.header.colour'
      :title='$store.state.header.title'
      :subtitle='$store.state.header.subtitle'
    ></main-header>
    <router-view :class="{'is-loading': $store.state.api.checkingStatus}"/>
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

<style>
  #main-container {
    margin-top: 20px;
  }
</style>

<style lang="scss">
  .is-loading {
    position: relative;
    pointer-events: none;
    opacity: 0.5;
    &:after {
        -webkit-animation: spinAround 500ms infinite linear;
        animation: spinAround 500ms infinite linear;
        border: 2px solid #dbdbdb;
        border-radius: 290486px;
        border-right-color: transparent;
        border-top-color: transparent;
        content: "";
        display: block;
        height: 1em;
        position: relative;
        width: 1em;

        position: absolute;
        top: calc(50% - 2.5em);
        left: calc(50% - 2.5em);
        width: 5em;
        height: 5em;
        border-width: 0.25em;
    }
  }
</style>
