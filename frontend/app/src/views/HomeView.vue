<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router' // 1. Import the router

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout() // 2. Call the store's action
  router.push('/login') // 3. Redirect
}
</script>

<template>
  <main>
    <h1>Welcome to your Finance App!</h1>
    
    <div v-if="authStore.isAuthenticated">
      <p>You are logged in.</p>
      
      <button @click="handleLogout">Logout</button>
      
    </div>
    <div v-else>
      <p>You are not logged in. Please go to the Login page.</p>
    </div>
  </main>
</template>

<style scoped>
main {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
}
button {
  padding: 10px 15px;
  background-color: #e63946; /* A red color */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>