<script setup>
import NoticiaDetalle from '@/components/NoticiaDetalle.vue'
import VolverBoton from '@/components/VolverBoton.vue'
</script>

<template>
  <main class="space-y-2">
    <VolverBoton></VolverBoton>
    <NoticiaDetalle :id="$route.params.id"></NoticiaDetalle>
  </main>
</template>
