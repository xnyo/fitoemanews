<template>
  <div id="app">
    <navbar></navbar>
    <main-header
      :colour='$store.state.header.colour'
      :title='$store.state.header.title'
      :subtitle='$store.state.header.subtitle'
    ></main-header>
    <simple-message-page
      v-if="!$store.state.api.checkingStatus && $store.state.api.offline"
      title="Qualcosa non va..."
      icon="fa-fire-extinguisher"
      colour="danger"
    >
      Sembra esserci un errore con il server. Per favore ritorna più tardi.
    </simple-message-page>
    <router-view v-else-if="!$store.state.loggingIn && !$store.state.api.checkingStatus" ref="view"></router-view>
    <div id="login-container" class="notification container is-widescreen" v-else>
      <div class="is-loading">
      </div>
    </div>
  </div>
</template>

<script>
import SimpleMessagePage from '@/components/SimpleMessagePage.vue'
import MainHeader from '@/components/MainHeader.vue'
import Navbar from '@/components/Navbar.vue'

export default {
  components: {
    MainHeader,
    Navbar,
    SimpleMessagePage
  }
}
</script>

<style>
  #main-container {
    margin-top: 20px;
  }

  #login-container {
    margin-top: 20px;
    height: 200px;
  }

  #login-container>div {
    height: 100%;
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
  .form-container.wide {
    width: 50%;
  }
  .ttitle {
    text-align: center !important;
    width: 100% !important ;
  }
  .progress::-webkit-progress-value {
    transition: all 0.5s ease;
  }
  .progress::-moz-progress-bar {
    transition: all 0.5s ease;
  }
  .form-container>span:first-child>i.fas {
    margin: 10px;
  }

  .form-container>span:first-child {
    margin-bottom: 10px;
  }
  .hide-children * {
    visibility: hidden !important;
  }
  .avatar {
    border-radius: 50%;
    margin-right: 10px;
  }
  .pagination-link, .pagination-previous, .pagination-next {
    text-decoration: none !important;
  }
  .notification a:not(.button) {
    text-decoration: none !important;
  }

  .not-visible {
    visibility: hidden;
  }

  .form-container .button[type="submit"] {
    width: 100%;
    margin-top: 10px;
  }

  .centered-msg-content {
    text-align: center;
  }
  .centered-msg-content p {
    margin-bottom: 20px;
  }

  /* Mobile */
  @media only screen and (max-width: 991px) {
    .form-container, .form-container.wide {
      width: 100%;
    }
    .navbar-item {
      color: white !important;
    }
  }

  /* Desktop */
  @media only screen and (min-width: 992px) and (max-width: 1599px) {
    .form-container {
      width: 50%;
    }
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
  $darker-blue: darken($dark-blue, 5%);
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

  @media only screen and (max-width: 1087px) {
    .navbar-link>img, .navbar-link>span {
      vertical-align: middle;
    }

    .navbar-item:not(.has-dropdown):hover, .navbar-link:hover {
      // color: white !important;
      background-color: $darker-blue !important;
    }
    .navbar-item, .navbar-link {
      color: white !important;
    }
  }

  // Import Bulma and Buefy styles
  @import "~bulma";
  @import "~buefy/src/scss/buefy";
</style>
