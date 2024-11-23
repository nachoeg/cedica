<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import FooterComponent from './components/FooterComponent.vue'
</script>

<template>
  <Navbar />
  <main class="max-w-[90rem] w-full mx-auto p-2 sm:p-5 lg:px-8">
    <RouterView />
  </main>
  <FooterComponent />
</template>
