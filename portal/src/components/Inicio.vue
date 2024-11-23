

<template>
<div class="home-container min-h-screen flex items-center justify-center"> 
  <div class="home-content text-center text-white bg-black bg-opacity-50 p-8 rounded"> 

    <h1 class="text-6xl font-bold mb-4">Somos CEDICA</h1> 
    
    <p class="text-2xl italic">Centro de Equitación para Personas con Discapacidad y Carenciadas</p>
    <p class="text-2xl">Brindamos rehabilitación ecuestre para mejorar la calidad de vida de nuestros usuarios.</p>

    <button class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 mt-8 rounded">
      <RouterLink to="/quienes_somos">Más información</RouterLink>
    </button>

  </div>
</div>

</template>

<script>
  export default {
    name: 'InicioComponent',
  }
</script>

