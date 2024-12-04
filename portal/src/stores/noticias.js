import { defineStore } from 'pinia'

export const useNoticiasStore = defineStore('noticias', {
  state: () => ({
    noticias: [],
    loading: false,
    error: null,
    cant_pages: 0,
    page: 1,
    per_page: 5,
    author: '',
    published_from: '',
    published_to: '',
  }),
  actions: {
    async fetchNoticias(
      page = 1,
      author = this.author,
      published_from = this.published_from,
      published_to = this.published_to,
      per_page = this.per_page,
    ) {
      try {
        this.loading = true
        this.error = null
        this.author = author
        this.published_from = published_from
        this.published_to = published_to

        const url = new URL('https://admin-grupo17.proyecto2024.linti.unlp.edu.ar/api/articles')

        if (author) url.searchParams.append('author', author)
        if (published_from) {
          url.searchParams.append('published_from', new Date(published_from).toISOString())
        }
        if (published_to)
          url.searchParams.append('published_to', new Date(published_to).toISOString())
        if (per_page) url.searchParams.append('per_page', per_page)
        if (page) url.searchParams.append('page', page)

        const response = await fetch(url)
        const data = await response.json()

        if (response.ok) {
          this.per_page = data.per_page
          this.cant_pages = data.cant_pages
          this.page = data.page
          this.noticias = data.data
        } else {
          this.error = data.error
        }
      } catch {
        this.error = 'Error al obtener las noticias'
      } finally {
        this.loading = false
      }
    },
  },
})
