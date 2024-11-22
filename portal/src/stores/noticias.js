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
        this.noticias = [
          {
            id: 1,
            titulo: 'titulo1',
            copete: 'copete1',
            contenido: 'contenido1',
            fecha_publicacion: 'fecha1',
            fecha_actualizacion: 'fecha1.1',
            autor: 'autor1',
            estado: 'borrador'
          },
          {
            id: 2,
            titulo: 'titulo2',
            copete: 'copete2',
            contenido: 'contenido2',
            fecha_publicacion: 'fecha2',
            fecha_actualizacion: 'fecha2.2',
            autor: 'autor2',
            estado: 'borrador'
          },
          {
            id: 3,
            titulo: 'titulo3',
            copete: 'copete3',
            contenido: 'contenido3',
            fecha_publicacion: 'fecha3',
            fecha_actualizacion: 'fecha3.3',
            autor: 'autor3',
            estado: 'borrador'
          },
          {
            id: 4,
            titulo: 'titulo4',
            copete: 'copete4',
            contenido: 'contenido4',
            fecha_publicacion: 'fecha4',
            fecha_actualizacion: 'fecha4.4',
            autor: 'autor4',
            estado: 'borrador'
          },
        ]

      } catch {
        this.error = 'Error al obtener las noticias'
      } finally {
        this.loading = false
      }
    }
  }
})
