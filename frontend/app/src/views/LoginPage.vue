<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)

const handleLogin = async () => {
    loading.value = true
    errorMessage.value = ''
    try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/token/`, {
            username: username.value,
            password: password.value
        })

        const accessToken = response.data.access
        authStore.setToken(accessToken)
        router.push('/')
    } catch (error) {
        console.error('Error logging in:', error)
        errorMessage.value = 'Invalid username or password.'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="auth-container">
        <div class="auth-card">
            <div class="header">
                <h1>Welcome Back</h1>
                <p>Please sign in to your account</p>
            </div>

            <form @submit.prevent="handleLogin" class="auth-form">
                <div class="input-group">
                    <label for="username">Username</label>
                    <input 
                        type="text" 
                        id="username" 
                        v-model="username" 
                        placeholder="Enter your username"
                        required 
                    />
                </div>

                <div class="input-group">
                    <label for="password">Password</label>
                    <input 
                        type="password" 
                        id="password" 
                        v-model="password" 
                        placeholder="Enter your password"
                        required
                    />
                </div>

                <div class="input-group forgot-password-link">
                    <router-link to="/forgot-password" class="link">Forgot Password?</router-link>
                </div>

                <button type="submit" class="submit-btn" :disabled="loading">
                    {{ loading ? 'Signing In...' : 'Log In' }}
                </button>

                <p v-if="errorMessage" class="error-message">
                    {{ errorMessage }}
                </p>
            </form>

            <div class="footer">
                <p>Don't have an account?</p>
                <router-link to="/register" class="link">Create Account</router-link>
            </div>
        </div>
    </div>
</template>

<style scoped>
.auth-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #f5f5f5;
    padding: 20px;
}

.auth-card {
    background: white;
    width: 100%;
    max-width: 400px;
    padding: 40px 30px;
    border-radius: 24px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
}

.header {
    text-align: center;
    margin-bottom: 30px;
}

.header h1 {
    font-size: 1.8rem;
    font-weight: 700;
    color: #333;
    margin-bottom: 8px;
}

.header p {
    color: #888;
    font-size: 0.95rem;
}

.auth-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.input-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.input-group label {
    font-size: 0.9rem;
    font-weight: 600;
    color: #555;
    margin-left: 4px;
}

.input-group input {
    width: 100%;
    padding: 14px 16px;
    background-color: #f9f9f9;
    border: 1px solid #eee;
    border-radius: 12px;
    font-size: 1rem;
    transition: all 0.2s;
    outline: none;
}

.input-group input:focus {
    background-color: white;
    border-color: #4991de;
    box-shadow: 0 0 0 3px rgba(73, 145, 222, 0.1);
}

.submit-btn {
    margin-top: 10px;
    padding: 16px;
    background-color: #4991de;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: background-color 0.2s;
}

.submit-btn:hover {
    background-color: #3b7bc4;
}

.submit-btn:disabled {
    background-color: #a0c3e8;
    cursor: not-allowed;
}

.error-message {
    color: #ff4d4d;
    font-size: 0.9rem;
    text-align: center;
    background: #ffe6e6;
    padding: 10px;
    border-radius: 8px;
}

.footer {
    margin-top: 30px;
    text-align: center;
    font-size: 0.9rem;
    color: #888;
}

.footer .link {
    color: #4991de;
    font-weight: 600;
    text-decoration: none;
    margin-left: 5px;
}

.footer .link:hover {
    text-decoration: underline;
}

.forgot-password-link {
    text-align: right;
    margin-top: -10px;
}
</style>