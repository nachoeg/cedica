<template>
  <div class="space-y-2 max-w-xl mx-auto">
    <!-- Titulo y filtros -->
    <div class="flex justify-between">
      <div class="flex gap-2 items-center">
        <h2 class="text-2xl font-bold">Noticias</h2>
        <LoadingComponent class="size-[16px]" v-if="loading" />
      </div>
      <div class="flex gap-2 items-center">
        <NoticiasCantidad :cantidad="per_page" @cantidad-changed="handleCantidadChanged" />
        <NoticiasFiltros
          @filtro-changed="handleFiltroChanged"
          :author="author"
          :published_from="published_from"
          :published_to="published_to"
        />
      </div>
    </div>

    <!-- Error al cargar noticias -->
    <div v-if="error" class="space-y-2">
      <p class="alert alert-error">{{ error }}</p>
      <button class="btn btn-outline" @click="handleRecargar">Volver a intentar</button>
    </div>

    <!-- Placeholder de noticias durante la carga -->
    <div v-if="loading" class="flex flex-col gap-2">
      <div v-for="page in per_page" :key="page" class="noticia">
        <div class="noticia-body space-y-2">
          <p class="skeleton h-6 w-1/2"></p>
          <p class="skeleton w-20"></p>
          <p class="skeleton"></p>
          <p class="skeleton"></p>
        </div>
        <div class="noticia-footer">
          <p class="skeleton w-3/5"></p>
        </div>
      </div>
    </div>

    <!-- Noticias -->
    <div v-if="!loading && noticias.length" class="flex flex-col gap-2">
      <RouterLink
        v-for="noticia in noticias"
        :to="{ name: 'noticia', params: { id: noticia.id } }"
        :key="noticia.id"
        class="noticia"
      >
        <div class="noticia-body">
          <h3 class="text-lg font-bold text-gray-800 dark:text-white">
            {{ noticia.title }}
          </h3>
          <p class="mt-1 text-xs font-medium uppercase text-gray-500 dark:text-neutral-400">
            {{ noticia.author }}
          </p>
          <p class="mt-2 text-gray-500 dark:text-neutral-300">
            {{ noticia.summary }}
          </p>
        </div>
        <div class="noticia-footer">
          <p class="mt-1 text-sm text-gray-500 dark:text-neutral-500">
            Fecha de publicacion: {{ formatFecha(noticia.published_at) }}
          </p>
          <p class="mt-1 text-sm text-gray-500 dark:text-neutral-500">
            Última actualización: {{ formatFecha(noticia.updated_at) }}
          </p>
        </div>
      </RouterLink>
    </div>

    <!-- No hay noticias -->
    <p v-if="!loading && !noticias.length && !error">No hay noticias para mostrar.</p>

    <!-- Paginación -->
    <NoticiasPaginacion
      v-if="!loading && cant_pages > 1"
      :cant_pages="cant_pages"
      :current_page="page"
      @page-changed="fetchNoticias"
    />
  </div>
</template>

<script setup>
import { useNoticiasStore } from '../stores/noticias.js'
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'
import LoadingComponent from '../components/LoadingComponent.vue'
import { RouterLink } from 'vue-router'
import NoticiasPaginacion from '../components/NoticiasPaginacion.vue'
import NoticiasFiltros from './NoticiasFiltros.vue'
import NoticiasCantidad from '../components/NoticiasCantidad.vue'

const formatFecha = (fecha) => {
  const opciones = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(fecha).toLocaleDateString('es-ES', opciones)
}

const store = useNoticiasStore()
const {
  noticias,
  cant_pages,
  page,
  per_page,
  author,
  published_from,
  published_to,
  loading,
  error,
} = storeToRefs(store)

const fetchNoticias = async (
  page = 1,
  author = '',
  published_from = '',
  published_to = '',
  per_page,
) => {
  await store.fetchNoticias(page, author, published_from, published_to, per_page)
}

const handleFiltroChanged = ({ autor, fechaInicio, fechaFin }) => {
  fetchNoticias(1, autor, fechaInicio, fechaFin, per_page.value)
}

const handleCantidadChanged = (cantidad) => {
  fetchNoticias(1, author.value, published_from.value, published_to.value, cantidad)
}

const handleRecargar = () => {
  fetchNoticias(page.value, author.value, published_from.value, published_to.value, per_page.value)
}

onMounted(() => {
  if (!noticias.value.length) {
    fetchNoticias(1, author.value, published_from.value, published_to.value, per_page.value)
  }
})
</script>
