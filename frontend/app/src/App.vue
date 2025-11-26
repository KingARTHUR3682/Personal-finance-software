<script setup>
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useExpenseStore } from './stores/expenseStore'

const authStore = useAuthStore()
const expenseStore = useExpenseStore()

onMounted(() => {
    // 1. Try to sync pending items immediately when app opens
    expenseStore.processQueue()

    // 2. Listen for "Internet Restored" event
    // This happens when toggle Airplane mode OFF or reconnect to WiFi
    window.addEventListener('online', () => {
        console.log("Back online! Syncing data...")
        expenseStore.processQueue()     // Upload queued offline items
        expenseStore.fetchInitialData() // Fetch latest data from server
    })
})
</script>

<template>
  <div class="app-container">
    <main class="content-area">
      <RouterView v-slot="{ Component }">
        <Transition name="fade" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
      </main>

    <nav v-if="authStore.isAuthenticated" class="bottom-nav">
      <router-link to="/" class="nav-item">
        <span>📝</span>
        <span class="label">Record</span>
      </router-link>
      <router-link to="/profile" class="nav-item">
        <span>👤</span>
        <span class="label">Profile</span>
      </router-link>
    </nav>
  </div>
</template>

<style scoped>
.content-area {
  padding-bottom: 80px; 
  min-height: 100vh;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background: white;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
  z-index: 1000;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
  padding-top: 12px;
  padding-bottom: calc(env(safe-area-inset-bottom) + 15px); 
  min-height: 85px;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #999;
  font-size: 0.8rem;
  text-decoration: none;
}

.nav-item.router-link-active {
  color: #eea838;
}
</style>