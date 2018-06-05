<template>
    <section class="hero is-primary" :class="[colourClass]">
        <div class="hero-body">
        <div class="container">
            <h1 class="title">
                {{ title }}
            </h1>
            <h2 class="subtitle">
                {{ subtitle }}
            </h2>
        </div>
        </div>
    </section>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: false,
      default: 'EmaNews'
    },
    subtitle: {
      type: String,
      required: false,
      default: ''
    },
    colour: {
      type: String,
      required: false,
      default: 'primary'
    }
  },
  computed: {
    colourClass () {
      return `is-${this.colour}`
    }
  }
}
</script>
