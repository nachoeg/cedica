<template>
  <Presentacion />
  <Tareas />
  <Areas />
</template>

<script>
import Presentacion from '../components/Presentacion.vue'
import Tareas from '../components/Tareas.vue'
import Areas from '../components/Areas.vue'

export default {
  components: {
    Presentacion,
    Tareas,
    Areas,
  },
}
</script>