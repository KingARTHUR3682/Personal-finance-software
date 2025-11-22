import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
import DashboardView from '../views/DashboardView.vue'
import RegisterPage from '../views/RegisterPage.vue'
import ExpenseDetailView from '@/views/ExpenseDetailView.vue'
import ProfileView from '@/views/ProfileView.vue'
import AddCategoryView from '@/views/AddCategoryView.vue'
import ForgotPasswordRequest from '@/views/ForgotPasswordRequest.vue'
import PasswordResetConfirm from '@/views/PasswordResetConfirm.vue'

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
      path: '/forgot-password',
      name: 'forgot-password-request',
      component: ForgotPasswordRequest,
    },
    {
      // This route captures the uidb64 and token from the email link
      path: '/reset-password/:uidb64/:token',
      name: 'password-reset-confirm',
      component: PasswordResetConfirm,
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
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true }
    },
    {
      path: '/category/add',
      name: 'add-category',
      component: AddCategoryView,
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
