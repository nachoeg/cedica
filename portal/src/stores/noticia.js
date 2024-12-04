import { defineStore } from 'pinia'

export const useNoticiaStore = defineStore('noticia', {
  state: () => ({
    noticia: {},
    loading: false,
    error: null,
  }),
  actions: {
    async fetchNoticia(id) {
      try {
        this.loading = true
        this.error = null

        const response = await fetch(
          `https://admin-grupo17.proyecto2024.linti.unlp.edu.ar/api/article?id=${id}`,
        )
        const data = await response.json()
        if (response.ok) {
          this.noticia = data
        } else {
          this.error = data.error
        }
      } catch {
        this.error = 'Error al obtener la noticia'
      } finally {
        this.loading = false
      }
    },
  },
})
