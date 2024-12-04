<script setup>
import { defineProps, defineEmits } from 'vue'
import IconChevronLeft from './icons/IconChevronLeft.vue'
import IconChevronRight from './icons/IconChevronRight.vue'

defineProps({
  cant_pages: {
    type: Number,
    required: true,
  },
  current_page: {
    type: Number,
    required: true,
  },
})

const emit = defineEmits(['page-changed'])

const changePage = (page) => {
  emit('page-changed', page)
}
</script>
<template>
  <nav class="flex items-center -space-x-px btn-group" aria-label="Pagination">
    <button
      type="button"
      aria-label="Anterior"
      :disabled="current_page === 1"
      @click="changePage(current_page - 1)"
    >
      <IconChevronLeft class="shrink-0 size-3.5" />
      <span class="hidden sm:block">Anterior</span>
    </button>
    <button
      v-for="page in cant_pages"
      :key="page"
      type="button"
      :aria-current="current_page === page ? 'page' : null"
      :class="{
        'bg-gray-200 dark:bg-neutral-700': current_page === page,
      }"
      @click="changePage(page)"
    >
      {{ page }}
    </button>
    <button
      type="button"
      aria-label="Siguiente"
      :disabled="current_page === cant_pages"
      @click="changePage(current_page + 1)"
    >
      <span class="hidden sm:block">Siguiente</span>
      <IconChevronRight class="shrink-0 size-3.5" />
    </button>
  </nav>
</template>
