import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
import DashboardView from '../views/DashboardView.vue'
import RegisterPage from '../views/RegisterPage.vue'
import ExpenseDetailView from '@/views/ExpenseDetailView.vue'
import ProfileView from '@/views/ProfileView.vue'

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
      component: DashboardView,
      meta: {requiresAuth: true}
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterPage
    },
    {
      path: '/expense/:id',
      name: 'expense-detail',
      component: ExpenseDetailView,
      meta: { requiresAuth: true }
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true }
    },
  ],
})

router.beforeEach((to, from, next) => {
    const publicPages = ['/login', '/register']
    const authRequired = !publicPages.includes(to.path)
    const loggedIn = localStorage.getItem('access_token')

    if (authRequired && !loggedIn) {
      next('/login')
    } else {
      next()
    }
})



export default router
