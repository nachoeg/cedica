

<template>
<div class="home-container min-h-screen flex items-center justify-center"> 
  <div class="home-content text-center text-white bg-black bg-opacity-40 p-8 rounded"> 

    <h1 class="text-5xl font-bold mb-4">Somos CEDICA</h1> 
    
    <p class="text-xl italic">Centro de Equitación para Personas con Discapacidad y Carenciadas</p>
    <p class="text-xl">Brindamos rehabilitación ecuestre para mejorar la calidad de vida de nuestros usuarios.</p>

    <button class="bg-[rgba(67,140,147,1)] hover:bg-[rgba(47,120,127,1)] text-white text-lg py-2 px-4 mt-8 rounded">
      <RouterLink to="/informacion">Más información</RouterLink>
    </button>

  </div>
</div>

</template>

<script>
  export default {
    name: 'InicioComponent',
  }
</script>

