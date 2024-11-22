<template>
  <div>
    <h2>Lista de noticias</h2>
    <p v-if="loading">Cargando...</p>
    <p v-if="error">{{ error }}</p>

    <table v-if="!loading && noticias.length">
      <thead>
      <tr>
        <th>#</th>
        <th>Titulo</th>
        <th>Copete</th>
        <th>Autor</th>
        <th>Fecha de publicación</th>
      </tr>
      </thead>
      <tbody>
        <tr v-for="noticia in noticias" :key="noticia.id">
          <td>{{ noticia.id }}</td>
          <td>{{ noticia.titulo }}</td>
          <td>{{ noticia.copete }}</td>
          <td>{{ noticia.autor }}</td>
          <td>{{ noticia.fecha_publicacion }}</td>
        </tr>
      </tbody>
    </table>
    <p v-if="!loading && !noticias.length">No hay noticias para mostrar.</p>
  </div>
</template>

<script setup>
import { useNoticiasStore } from '../stores/noticias.js';
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue';

const store = useNoticiasStore();
const { noticias, loading, error } = storeToRefs(store);

const fetchNoticias = async() => {
  await store.fetchNoticias();
};

onMounted(() => {
  console.log("HOla");
  if (!noticias.value.length) {
    fetchNoticias();
  }
});
</script>
