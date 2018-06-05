<template>
  <div>
    <div id="main-container" class="container is-widescreen">
      <div class="notification ">
        Homepage
      </div>
    </div>
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
