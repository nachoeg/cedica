<template>
  <div class="space-y-2 max-w-xl mx-auto">
    <h2 class="text-2xl font-bold">Noticias</h2>
    <LoadingComponent v-if="loading"></LoadingComponent>
    <p v-if="error">{{ error }}</p>
    <div v-if="!loading && noticias.length" class="flex flex-col gap-2">
      <a
        v-for="noticia in noticias"
        :key="noticia.id"
        :href="`/noticias/${noticia.id}`"
        class="flex flex-col bg-white border shadow-sm rounded-xl dark:bg-neutral-800 dark:border-neutral-700"
      >
        <div class="p-4 md:p-5">
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
        <div
          class="bg-gray-100 border-t rounded-b-xl py-3 px-4 md:py-4 md:px-5 dark:bg-neutral-800 dark:border-neutral-700"
        >
          <p class="mt-1 text-sm text-gray-500 dark:text-neutral-500">
            Última actualización {{ noticia.updated_at }}
          </p>
        </div>
      </a>
    </div>
    <p v-if="!loading && !noticias.length">No hay noticias para mostrar.</p>
  </div>
</template>

<script setup>
import { useNoticiasStore } from '../stores/noticias.js'
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'
import LoadingComponent from '../components/LoadingComponent.vue'

const store = useNoticiasStore()
const { noticias, loading, error } = storeToRefs(store)

const fetchNoticias = async () => {
  await store.fetchNoticias()
}

onMounted(() => {
  if (!noticias.value.length) {
    fetchNoticias()
  }
})
</script>
