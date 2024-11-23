<template>
  <Inicio class="inicio rounded-xl" />
</template>

<script>
import Inicio from '../components/Inicio.vue'

export default {
  components: {
    Inicio,
  },
}
</script>

<style scoped>
.inicio {
  background-image: url('@/assets/background.jpg');
  background-position: center bottom;
  background-color: rgba(0, 0, 0, 0.3);
  background-blend-mode: overlay;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 100vh;
  min-height: 100vh;
  margin: 0;
  padding: 0;
}
</style>
