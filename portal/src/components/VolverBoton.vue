<script setup>
import IconChevronLeft from '@/components/icons/IconChevronLeft.vue'
import { RouterLink } from 'vue-router'
</script>
<template>
  <RouterLink to="/noticias" class="btn btn-outline gap-0.5 py-1.5 px-2">
    <IconChevronLeft class="size-4" />
    <span class="pe-1">Volver</span>
  </RouterLink>
</template>
