<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const email = ref('')
const message = ref('')
const loading = ref(false)
const error = ref('')

// This URL maps to the /api/auth/password_reset/ endpoint configured in the backend.
const BACKEND_URL = 'http://192.168.100.40:8000/api/auth/password_reset/'

const handleRequest = async () => {
    loading.value = true
    message.value = ''
    error.value = ''

    try {
        await axios.post(BACKEND_URL, { email: email.value })

        message.value = 'If an account with that email exists, we have sent a password reset link.'
    } catch (err) {
        console.error('Error requesting password reset:', err)
        error.value = 'Failed to request reset. Please try again.'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="auth-container">
        <div class="auth-card">
            <div class="header">
                <h1>Forgot Password</h1>
                <p>Enter your email to receive a password reset link.</p>
            </div>

            <form @submit.prevent="handleRequest" class="auth-form">
                <div class="input-group">
                    <label for="email">Email Address</label>
                    <input 
                        type="email" 
                        id="email" 
                        v-model="email" 
                        placeholder="Enter your email"
                        required 
                    />
                </div>

                <button type="submit" class="submit-btn" :disabled="loading">
                    {{ loading ? 'Sending...' : 'Request Reset Link' }}
                </button>

                <p v-if="message" class="success-message">
                    {{ message }}
                </p>
                <p v-if="error" class="error-message">
                    {{ error }}
                </p>
            </form>

            <div class="footer">
                <router-link to="/login" class="link">Back to Log In</router-link>
            </div>
        </div>
    </div>
</template>

<style scoped>
.auth-container { min-height: 100vh; display: flex; align-items: center; justify-content: center; background-color: #f5f5f5; padding: 20px; }
.auth-card { background: white; width: 100%; max-width: 400px; padding: 40px 30px; border-radius: 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
.header { text-align: center; margin-bottom: 30px; }
.header h1 { font-size: 1.8rem; font-weight: 700; color: #333; margin-bottom: 8px; }
.header p { color: #888; font-size: 0.95rem; }
.auth-form { display: flex; flex-direction: column; gap: 20px; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group label { font-size: 0.9rem; font-weight: 600; color: #555; margin-left: 4px; }
.input-group input { width: 100%; padding: 14px 16px; background-color: #f9f9f9; border: 1px solid #eee; border-radius: 12px; font-size: 1rem; transition: all 0.2s; outline: none; }
.input-group input:focus { background-color: white; border-color: #4991de; box-shadow: 0 0 0 3px rgba(73, 145, 222, 0.1); }
.submit-btn { margin-top: 10px; padding: 16px; background-color: #4991de; color: white; border: none; border-radius: 12px; font-size: 1rem; font-weight: 700; cursor: pointer; transition: background-color 0.2s; }
.submit-btn:hover { background-color: #3b7bc4; }
.submit-btn:disabled { background-color: #a0c3e8; cursor: not-allowed; }
.error-message { color: #ff4d4d; font-size: 0.9rem; text-align: center; background: #ffe6e6; padding: 10px; border-radius: 8px; }
.success-message { color: #42b983; font-size: 0.9rem; text-align: center; background: #e6fff0; padding: 10px; border-radius: 8px; }
.footer { margin-top: 30px; text-align: center; font-size: 0.9rem; color: #888; }
.footer .link { color: #4991de; font-weight: 600; text-decoration: none; }
.footer .link:hover { text-decoration: underline; }
</style>