import { defineStore } from 'pinia'

export const useNoticiasStore = defineStore('noticias', {
  state: () => ({
    noticias: [],
    loading: false,
  }),
  actions: {
    async fetchNoticias() {
      //obtiene las noticias
      try {
        this.loading = true
        this.error = null
        const response = await fetch('http://localhost:5000/api/articles')
        if (response.ok) {
          const data = await response.json();
          console.log(data);
          this.noticias = data.data;
        }
      } catch {
        this.error = 'Error al obtener las noticias'
      } finally {
        this.loading = false
      }
    },
  },
})
