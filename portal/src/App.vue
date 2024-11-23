<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
</script>

<template>
  <Navbar />
  <main class="inicio bg-left w-full mx-auto p-2 sm:p-5 lg:px-8">
    <RouterView />
  </main>
  <Footer />
</template>


<style scoped> 
.inicio { 
  background-image: url('@/assets/background.jpg'); 
  background-position: center bottom;
  background-color: rgba(0, 0, 0, 0.3); 
  background-blend-mode: overlay; 
  background-size: cover; background-position: center; 
  background-repeat: no-repeat;
  height: 100vh;
  min-height: 100vh;
  margin: 0;
  padding: 0;
  } 
</style>