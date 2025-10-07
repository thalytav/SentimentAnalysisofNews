import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/views/LandingPage.vue'
import AnalysisPage from '@/views/AnalysisPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: LandingPage,
    },

    {
      path: '/analyze',
      name: 'analyze',
      component: AnalysisPage,
    },
  ],
})

export default router
