<script setup>
import { useNoticiaStore } from '@/stores/noticia'
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'
import LoadingComponent from '@/components/LoadingComponent.vue'

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
})

const store = useNoticiaStore()
const { noticia, loading, error } = storeToRefs(store)

const fetchNoticia = async () => {
  await store.fetchNoticia(props.id)
}

onMounted(() => {
  fetchNoticia()
})
</script>
<template>
  <div
    class="w-full bg-white border shadow-sm rounded-xl dark:bg-neutral-800 dark:border-neutral-700 p-4 md:p-5"
  >
    <p v-if="error">{{ error }}</p>
    <div v-if="loading" class="p-20 flex justify-center">
      <LoadingComponent></LoadingComponent>
    </div>
    <div v-if="!loading && noticia">
      <h1 class="text-xl sm:text-3xl font-bold">{{ noticia.title }}</h1>
      <p class="text-gray-600 dark:text-neutral-400">{{ noticia.author }}</p>
      <br />
      <h2 class="sm:text-xl">{{ noticia.summary }}</h2>
      <br />
      <p>{{ noticia.content }}</p>
      <br />
      <div class="text-gray-600 dark:text-neutral-400 text-end">
        <p>Fecha de publicación: {{ noticia.published_at }}</p>
        <p>Última actualización: {{ noticia.updated_at }}</p>
      </div>
    </div>
  </div>
</template>
