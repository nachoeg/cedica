<script setup>
import IconFilter from '../components/icons/IconFilter.vue'
import { defineEmits, defineProps, ref, computed } from 'vue'

const emit = defineEmits(['filtro-changed'])

const props = defineProps({
  author: {
    type: String,
    default: '',
  },
  published_from: {
    type: String,
    default: '',
  },
  published_to: {
    type: String,
    default: '',
  },
})

const autor = ref(props.author)
const fechaInicio = ref(props.published_from)
const fechaFin = ref(props.published_to)

const filtrarTabla = () => {
  emit('filtro-changed', {
    autor: autor.value,
    fechaInicio: fechaInicio.value,
    fechaFin: fechaFin.value,
  })
}

const limpiarFiltros = () => {
  autor.value = ''
  fechaInicio.value = ''
  fechaFin.value = ''
  emit('filtro-changed', { autor: '', fechaInicio: '', fechaFin: '' })
}

const filtrosActivos = computed(() => {
  let count = 0
  if (autor.value) count++
  if (fechaInicio.value) count++
  if (fechaFin.value) count++
  return count
})
</script>
<template>
  <div
    class="hs-dropdown [--auto-close:inside] [--placement:bottom-right] relative inline-flex z-20"
  >
    <button
      id="hs-dropdown-filtro"
      type="button"
      class="hs-dropdown-toggle btn btn-outline text-xs py-1.5 px-2.5 gap-x-1.5"
    >
      <IconFilter class="size-3.5 dark:text-neutral-300" />
      Filtrar
      <span
        v-if="filtrosActivos > 0"
        class="border-s dark:border-neutral-700 text-blue-500 ps-1.5"
        >{{ filtrosActivos }}</span
      >
    </button>

    <div
      class="dropdown hs-dropdown-menu transition-[opacity,margin] duration hs-dropdown-open:opacity-100 opacity-0 hidden max-w-xs"
      aria-labelledby="hs-dropdown-filtro"
    >
      <div class="[&_input]:mb-2 mb-2">
        <label for="filtro-autor" class="block text-sm dark:text-white"> Autor </label>
        <input
          type="text"
          id="filtro-autor"
          placeholder="Escriba un valor"
          @input="filtrarTabla"
          v-model="autor"
        />
        <label for="filtro-fecha-inicio" class="block text-sm dark:text-white">
          Publicado desde
        </label>
        <input type="date" id="filtro-fecha-inicio" @input="filtrarTabla" v-model="fechaInicio" />
        <label for="filtro-fecha-fin" class="block text-sm dark:text-white">
          Publicado hasta
        </label>
        <input type="date" id="filtro-fecha-fin" @input="filtrarTabla" v-model="fechaFin" />
      </div>
      <button type="button" @click="limpiarFiltros" class="btn btn-secondary w-full">
        Limpiar filtros
      </button>
    </div>
  </div>
</template>
