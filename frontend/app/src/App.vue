<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth' // Import the store

const authStore = useAuthStore() // Get the store instance
const router = useRouter()

const handleLogout = () => {
  authStore.logout() // Call the store's logout action
  router.push('/login') // Redirect to login
}
</script>

<template>
  <div class="mobile-wrapper">
    
    <!-- This is the main content area where your pages (Login, Dashboard) will show up -->
    <main class="content-area">
      <RouterView />
    </main>

    <!-- Bottom navigation bar -->
    <!-- It will ONLY show if user are logged in -->
    <nav v-if="authStore.isAuthenticated" class="bottom-nav">
      <RouterLink to="/">Home</RouterLink>
      <a @click="handleLogout" href="#">Logout</a>
    </nav>

  </div>
</template>

<style scoped>
.mobile-wrapper {
  max-width: 450px; /* A typical mobile screen width */
  height: 85vh; /* 85% of the viewport height */
  margin: 40px auto; /* Centers the phone on your desktop */
  
  border: 1px solid #555;
  border-radius: 20px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);

  /* This is the magic for pinning the nav to the bottom */
  display: flex;
  flex-direction: column;
}

/* This makes the page content (like your login form) fill the space */
.content-area {
  flex-grow: 1; /* This makes the content take all available vertical space */
  overflow-y: auto; /* This makes ONLY the content scrollable, not the whole app */
  padding: 20px;
}

/* --- Bottom Nav Bar Styles --- */
.bottom-nav {
  display: flex;
  justify-content: space-around; /* Evenly space the links */
  align-items: center;
  padding: 10px 0;
  border-top: 1px solid var(--color-border);
  background: var(--color-background-soft);
  
  /* Match the rounded corners of the phone */
  border-bottom-left-radius: 20px;
  border-bottom-right-radius: 20px;
}

.bottom-nav a {
  color: var(--color-text);
  text-decoration: none;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.1rem;
}

/* This highlights the active page link */
.bottom-nav a.router-link-exact-active {
  color: var(--color-heading);
  background-color: var(--color-background-mute);
}
</style>