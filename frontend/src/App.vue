<template>
  <div id="app">
    <navbar></navbar>
    <main-header
      :colour='$store.state.header.colour'
      :title='$store.state.header.title'
      :subtitle='$store.state.header.subtitle'
    ></main-header>
    <router-view :class="{'is-loading': $store.state.api.checkingStatus}"/>
  </div>
</template>

<script>
import MainHeader from '@/components/MainHeader.vue'
import Navbar from '@/components/Navbar.vue'

export default {
  components: {
    MainHeader,
    Navbar
  }
}
</script>

<style>
  #main-container {
    margin-top: 20px;
  }

  html {
    height: 100vh;
    min-height: 100vh;
    background-color: #F0F2F4 !important;
  }
  body {
    min-height: 100vh;
  }
  .text-centered {
    text-align: center;
  }
  .el-centered {
    width: 100%;
    margin: 0 auto;
  }

  .form-container {
    width: 30%;
    padding: 50px;
    margin: 50px auto 50px auto;
    border-radius: 5px;
    background-color: #fff;
    box-shadow: 0 2px 3px rgba(10, 10, 10, 0.1), 0 0 0 1px rgba(10, 10, 10, 0.1);
    color: #4a4a4a;
  }
  .ttitle {
    text-align: center !important;
    width: 100% !important ;
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


<style lang="scss">
  // Import Bulma's core
  @import "~bulma/sass/utilities/_all";

  // Set your colors
  $primary: #4099FF;
  $primary-invert: findColorInvert($primary);
  $info: #8c67ef;
  $info-invert: findColorInvert($info);
  $dark-blue: #3273dc;
  $dark-blue-invert: findColorInvert($dark-blue);

  // Setup $colors to use as bulma classes (e.g. 'is-twitter')
  $colors: (
      "white": ($white, $black),
      "black": ($black, $white),
      "light": ($light, $light-invert),
      "dark": ($dark, $dark-invert),
      "primary": ($primary, $primary-invert),
      "info": ($info, $info-invert),
      "success": ($success, $success-invert),
      "warning": ($warning, $warning-invert),
      "danger": ($danger, $danger-invert),
      "dark-blue": ($dark-blue, $dark-blue-invert)
  );

  // Links
  $link: $primary;
  $link-invert: $primary-invert;
  $link-focus-border: $primary;

  // Import Bulma and Buefy styles
  @import "~bulma";
  @import "~buefy/src/scss/buefy";
</style>
