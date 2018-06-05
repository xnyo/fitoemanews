<template>
  <div>
    Home
  </div>
</template>

<script>
export default {
  beforeMount () {
    this.$store.commit('setHeader', {
      subtitle: 'Homepage'
    })
  }
}
</script>
