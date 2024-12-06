<template>
  <Informacion />
  <Tareas />
  <Areas />
</template>

<script>
import Informacion from '../components/Informacion.vue'
import Tareas from '../components/Tareas.vue'
import Areas from '../components/Areas.vue'

export default {
  components: {
    Informacion,
    Tareas,
    Areas,
  },
}
</script>