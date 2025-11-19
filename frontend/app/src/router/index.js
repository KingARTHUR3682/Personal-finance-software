import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
import Dashboard from '../views/Dashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage
    },
    {
      path: '/',
      name: 'home',
      component: Dashboard,
      meta: {requiresAuth: true}
    }
  ],
})

router.beforeEach((to, from, next) => {
    const publicPages = ['/login']
    const authRequired = !publicPages.includes(to.path)
    const loggedIn = localStorage.getItem('access_token')

    if (authRequired && !loggedIn) {
      next('/login')
    } else {
      next()
    }
})



export default router
