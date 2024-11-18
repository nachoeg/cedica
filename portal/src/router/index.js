import { createRouter, createWebHistory } from 'vue-router'
import InicioView from '../views/InicioView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'inicio',
      component: InicioView,
    },
    {
      path: '/noticias',
      name: 'noticias',
      component: () => import('../views/NoticiasView.vue'),
    },
    {
      path: '/contacto',
      name: 'contacto',
      component: () => import('../views/ContactoView.vue'),
    },
  ],
})

router.afterEach((to, from, failure) => {
  if (!failure) {
    setTimeout(() => {
      window.HSStaticMethods.autoInit()
    }, 100)
  }
})

export default router
