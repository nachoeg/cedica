<script setup>
import { defineProps } from 'vue'

defineProps({
  href: {
    type: String,
    required: true,
  },
})
</script>
<template>
  <a
    class="size-8 inline-flex justify-center items-center gap-x-2 text-sm font-semibold rounded-full border border-transparent text-gray-500 hover:shadow hover:bg-white focus:outline-none focus:bg-white disabled:opacity-50 disabled:pointer-events-none dark:text-neutral-400 dark:hover:bg-neutral-700 dark:focus:bg-neutral-700"
    :href="href"
    target="_blank"
    rel="noopener"
  >
    <slot></slot>
  </a>
</template>
