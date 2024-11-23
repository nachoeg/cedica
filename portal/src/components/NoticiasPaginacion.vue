<script setup>
import { defineProps, defineEmits } from 'vue'

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
  <nav class="flex items-center -space-x-px" aria-label="Pagination">
    <button
      type="button"
      class="min-h-[38px] min-w-[38px] py-2 px-2.5 inline-flex justify-center items-center gap-x-1.5 text-sm first:rounded-s-lg last:rounded-e-lg border border-gray-200 text-gray-800 hover:bg-gray-100 focus:outline-none focus:bg-gray-100 disabled:opacity-50 disabled:pointer-events-none dark:border-neutral-700 dark:text-white dark:hover:bg-white/10 dark:focus:bg-white/10"
      aria-label="Anterior"
      :disabled="current_page === 1"
      @click="changePage(current_page - 1)"
    >
      <svg
        class="shrink-0 size-3.5"
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="m15 18-6-6 6-6"></path>
      </svg>
      <span class="hidden sm:block">Anterior</span>
    </button>
    <button
      v-for="page in cant_pages"
      :key="page"
      type="button"
      class="min-h-[38px] min-w-[38px] flex justify-center items-center text-gray-800 border border-gray-200 py-2 px-3 text-sm first:rounded-s-lg last:rounded-e-lg focus:outline-none disabled:opacity-50 disabled:pointer-events-none dark:border-neutral-700 dark:text-white"
      :aria-current="current_page === page ? 'page' : null"
      :class="{
        'bg-gray-200 focus:bg-gray-300 dark:bg-neutral-600 dark:focus:bg-neutral-500':
          current_page === page,
        'hover:bg-gray-100 focus:bg-gray-100 dark:hover:bg-white/10 dark:focus:bg-white/10':
          current_page !== page,
      }"
      @click="changePage(page)"
    >
      {{ page }}
    </button>
    <button
      type="button"
      class="min-h-[38px] min-w-[38px] py-2 px-2.5 inline-flex justify-center items-center gap-x-1.5 text-sm first:rounded-s-lg last:rounded-e-lg border border-gray-200 text-gray-800 hover:bg-gray-100 focus:outline-none focus:bg-gray-100 disabled:opacity-50 disabled:pointer-events-none dark:border-neutral-700 dark:text-white dark:hover:bg-white/10 dark:focus:bg-white/10"
      aria-label="Siguiente"
      :disabled="current_page === cant_pages"
      @click="changePage(current_page + 1)"
    >
      <span class="hidden sm:block">Siguiente</span>
      <svg
        class="shrink-0 size-3.5"
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="m9 18 6-6-6-6"></path>
      </svg>
    </button>
  </nav>
</template>
