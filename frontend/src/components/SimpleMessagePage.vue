<template>
  <div class="form-container">
    <span class="icon is-large ttitle" :class="colourClass">
      <i class="fas fa-2x" :class="icon"></i>
      <h3 class="title">{{ title }}</h3>
    </span>
    <slot></slot>
  </div>
</template>

<script>
export default {
  props: ['title', 'colour', 'icon'],
  computed: {
    colourClass () {
      return `has-text-${this.colour}`
    }
  }
}
</script>

<style>

</style>
