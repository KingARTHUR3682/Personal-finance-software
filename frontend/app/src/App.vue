<script setup>
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// Simple tab navigation logic can be added here later if needed
</script>

<template>
  <div class="app-container">
    <main class="content-area">
      <RouterView />
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
  padding-bottom: 80px; /* Space for bottom nav */
  min-height: 100vh;
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
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #999;
  font-size: 0.8rem;
}

.nav-item.router-link-active {
  color: #eea838; /* Yellow accent */
}
</style>