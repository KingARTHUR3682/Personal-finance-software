<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const user = ref(null)
const loading = ref(true)
const errorMessage = ref('')

onMounted(async () => {
  try {
    // Fetch the current user's details from the backend
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/profile/`, {
      headers: { Authorization: `Bearer ${authStore.token}` }
    })
    user.value = response.data
  } catch (error) {
    console.error('Error fetching profile:', error)
    errorMessage.value = 'Could not load profile details.'
  } finally {
    loading.value = false
  }
})

const handleLogout = () => {
  // Clear token and redirect
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="profile-page">
    <h2>User Profile</h2>

    <div v-if="loading" class="loading">Loading...</div>
    
    <div v-else-if="user" class="profile-card">
      <div class="avatar-placeholder">
        {{ user.username.charAt(0).toUpperCase() }}
      </div>
      
      <div class="info-group">
        <label>Username</label>
        <div class="info-value">{{ user.username }}</div>
      </div>

      <div class="info-group">
        <label>Email</label>
        <div class="info-value">{{ user.email }}</div>
      </div>

      <button class="logout-btn" @click="handleLogout">
        Log Out
      </button>
    </div>

    <div v-else class="error">
      {{ errorMessage }}
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  max-width: 500px;
  margin: 40px auto;
  padding: 20px;
  text-align: center;
}

h2 {
  margin-bottom: 30px;
  color: #333;
}

.profile-card {
  background: white;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar-placeholder {
  width: 80px;
  height: 80px;
  background-color: #4991de; /* Matches your login button color */
  color: white;
  font-size: 2.5rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin-bottom: 25px;
}

.info-group {
  width: 100%;
  text-align: left;
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.info-group label {
  font-size: 0.85rem;
  color: #888;
  display: block;
  margin-bottom: 5px;
}

.info-value {
  font-size: 1.1rem;
  font-weight: 500;
  color: #333;
}

.logout-btn {
  margin-top: 20px;
  padding: 12px 40px;
  background-color: transparent;
  color: #ff4d4d;
  border: 2px solid #ff4d4d;
  border-radius: 30px; /* Round bordered rectangle */
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
}

.logout-btn:hover {
  background-color: #ff4d4d;
  color: white;
}

.error {
  color: red;
}
</style>