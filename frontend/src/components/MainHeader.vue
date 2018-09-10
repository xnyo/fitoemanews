<template>
    <section class="hero is-primary">
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
    }
  },
  computed: {
    colourClass () {
      return `is-${this.colour}`
    }
  }
}
</script>
