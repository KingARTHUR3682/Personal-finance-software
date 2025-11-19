<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Get the Pinia store and the Vue router
const authStore = useAuthStore()
const router = useRouter()

// Create reactive varuables for the form fields
const username = ref('')
const password = ref('')
const errorMessage = ref('') // to show login errors

// -- Function --
const handleLogin = async () => {
    try {
        // Make the API call to Django backend
        const response = await axios.post('http://192.168.100.40:8000/api/token/', {
            username: username.value,
            password: password.value
        })

        // Get the access token from the response
        const accessToken = response.data.access
        
        // Save the token in Pinia store
        authStore.setToken(accessToken)

        router.push('/')
    } catch (error) {
        console.error('Error logging in:', error)
        errorMessage.value = 'Failed to login. Please check your username and password.'
    }
}
</script>

<template>
    <div class="login-page">
        <h2>Login</h2>
        <form @submit.prevent="handleLogin">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" />
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password"/>
            </div>
            <button type="submit">Login</button>
            <p v-if="errorMessage" class="error-message">
                {{ errorMessage }}
            </p>
        </form>
    </div>
</template>

<style scoped>


.login-page h2 {
    margin-bottom: 5px;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
}

.form-group input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
}

button {
    padding: 10px 15px;
    background-color: #4991de;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.error-message {
    color: red;
    font-size: 0.9em;
}
</style>