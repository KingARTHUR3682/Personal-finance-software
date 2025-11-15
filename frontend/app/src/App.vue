<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth' // 1. Import the store

const authStore = useAuthStore() // 2. Get the store instance
const router = useRouter()

const handleLogout = () => {
  authStore.logout() // 3. Call the store's logout action
  router.push('/login') // 4. Redirect to login
}
</script>

<template>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        
        <RouterLink v-if="!authStore.isAuthenticated" to="/login">
          Login
        </RouterLink>
        
        <a v-if="authStore.isAuthenticated" @click="handleLogout" href="#">
          Logout
        </a>
      </nav>
    </div>
  <RouterView />
</template>

<style scoped>
header {
  width: 100%;
  padding: 15px 0;
  border-bottom: 1px solid var(--color-border);
  background-color: var(--color-background);
}

nav {
  width: 100%;
  text-align: center;
  font-size: 1rem;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
  cursor: pointer;
}

nav a:first-of-type {
  border: 0;
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

.wrapper {
  position: fixed;
  top: 10px;
  left: 0;
  width: 100%;
  z-index: 1000;
}
</style>