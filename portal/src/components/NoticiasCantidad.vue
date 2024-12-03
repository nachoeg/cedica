<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  cantidad: {
    type: Number,
    required: true,
  },
})

const emit = defineEmits(['cantidad-changed'])

const changePerPage = (perPage) => {
  emit('cantidad-changed', perPage)
}

let opciones = [5, 10, 20]

if (!opciones.includes(props.cantidad)) {
  opciones.push(props.cantidad)
  opciones.sort((a, b) => a - b)
}
</script>
<template>
  <select
    class="input pe-8 py-1 bg-gray-50 dark:bg-neutral-900"
    @change="changePerPage($event.target.value)"
    :value="cantidad"
  >
    <option v-for="opcion in opciones" :key="opcion" :value="opcion">
      {{ opcion }}
    </option>
  </select>
</template>
