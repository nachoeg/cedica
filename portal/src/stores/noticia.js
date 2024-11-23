import { defineStore } from 'pinia'

export const useNoticiaStore = defineStore('noticia', {
  state: () => ({
    noticia: {},
    loading: false,
  }),
  actions: {
    async fetchNoticia(id) {
      try {
        this.loading = true
        const response = await fetch(`https://admin-grupo17.proyecto2024.linti.unlp.edu.ar/api/article?id=${id}`)
        if (response.ok) {
          const data = await response.json()
          this.noticia = data
        }
      } catch {
        this.error = 'Error al obtener la noticia'
      } finally {
        this.loading = false
      }
    },
  },
})
