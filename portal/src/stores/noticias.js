import { defineStore } from 'pinia'

export const useNoticiasStore = defineStore('noticias', {
  state: () => ({
    noticias: [],
    loading: false,
    cant_pages: 0,
    page: 1, // Página actual
    error: null,
  }),
  actions: {
    async fetchNoticias(page = 1) {
      // Obtiene las noticias para la página especificada
      try {
        this.loading = true
        this.error = null
        const response = await fetch(`http://localhost:5000/api/articles?page=${page}`)
        if (response.ok) {
          const data = await response.json()
          this.cant_pages = data.cant_pages
          this.page = data.page
          this.noticias = data.data
        }
      } catch {
        this.error = 'Error al obtener las noticias'
      } finally {
        this.loading = false
      }
    },
  },
})
