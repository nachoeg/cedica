<script setup>
let noticia = {
  id: 6,
  titulo: 'Vue 3 Composition API',
  copete: 'Nuevas formas de escribir componentes en Vue 3',
  contenido:
    'Usando Composition API para mejorar la reutilización de código. La Composition API en Vue 3 permite organizar el código de una manera más modular y reutilizable. Esto facilita la gestión de estados y lógica de negocio en componentes complejos, mejorando la mantenibilidad y escalabilidad de las aplicaciones. Además, la Composition API introduce nuevas funciones como `setup()`, `ref()`, `reactive()`, y `watch()`, que proporcionan un control más fino sobre el ciclo de vida de los componentes y la reactividad. Con estas herramientas, los desarrolladores pueden crear aplicaciones más robustas y fáciles de mantener. La adopción de la Composition API también abre la puerta a nuevas oportunidades para compartir y reutilizar lógica entre diferentes proyectos y equipos, promoviendo una mayor colaboración y consistencia en el desarrollo de software.',
  fecha_publicacion: '2023-05-10',
  fecha_actualizacion: '2023-05-12',
  autor: 'Luis Fernandez',
  estado: 'publicado',
}
</script>
<template>
  <div
    class="w-full bg-white border shadow-sm rounded-xl dark:bg-neutral-800 dark:border-neutral-700 p-4 md:p-5"
  >
    <h1 class="text-xl sm:text-3xl font-bold">{{ noticia.titulo }}</h1>
    <p class="text-gray-600 dark:text-neutral-400">{{ noticia.autor }}</p>
    <br />
    <h2 class="sm:text-xl">{{ noticia.copete }}</h2>
    <br />
    <p>{{ noticia.contenido }}</p>
    <br />
    <div class="text-gray-600 dark:text-neutral-400 text-end">
      <p>Fecha de publicación: {{ noticia.fecha_publicacion }}</p>
      <p>Última actualización: {{ noticia.fecha_actualizacion }}</p>
    </div>
  </div>
</template>
