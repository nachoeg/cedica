

<template>
<div class="home-container min-h-screen flex items-center justify-center"> 
  <div class="home-content text-center text-white bg-black bg-opacity-50 p-8 rounded"> 
  
    <h1 class="text-4xl font-bold mb-4">Somos CEDICA</h1> 
    <p class="text-lg">Un centro dedicado a la equinoterapia que proporciona terapias
     asistidas con caballos para mejorar la calidad de vida de nuestros usuarios.</p>

    <div class="flex flex-col btn-secondary">
      <RouterLink to="/quienes_somos">Más información</RouterLink>
    </div>

  </div>
</div>

</template>

<script>
  export default {
    name: 'InicioComponent',
  }
</script>

<style scoped> 
.home-container { 
  background-image: url('@/assets/background.jpg'); 
  background-color: rgba(0, 0, 0, 0.3); 
  background-blend-mode: overlay; 
  background-size: cover; background-position: center; 
  background-repeat: no-repeat; height: 100vh;
  } 
</style>