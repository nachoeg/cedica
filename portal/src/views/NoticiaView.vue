<script setup>
import NoticiaDetalle from '@/components/NoticiaDetalle.vue'
</script>

<template>
  <main>
    <NoticiaDetalle :id="$route.params.id"></NoticiaDetalle>
  </main>
</template>
