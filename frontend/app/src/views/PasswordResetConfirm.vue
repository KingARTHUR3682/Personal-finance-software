<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const uidb64 = ref('')
const token = ref('')
const newPassword1 = ref('')
const newPassword2 = ref('')
const message = ref('')
const loading = ref(false)
const error = ref('')

const BACKEND_URL_BASE = `${import.meta.env.VITE_API_URL}/api/auth/reset/`

onMounted(() => {
    // Extract uidb64 and token from the route params set in index.js
    uidb64.value = route.params.uidb64
    token.value = route.params.token
})

const handleReset = async () => {
    loading.value = true
    message.value = ''
    error.value = ''

    if (newPassword1.value !== newPassword2.value) {
        error.value = 'Passwords do not match.'
        loading.value = false
        return
    }

    try {
        // Construct the full URL for the Django PasswordResetConfirmView
        const url = `${BACKEND_URL_BASE}${uidb64.value}/${token.value}/`
        
        // Django's view expects new_password1 and new_password2 in the payload
        await axios.post(url, {
            new_password1: newPassword1.value,
            new_password2: newPassword2.value
        })

        message.value = 'Your password has been reset successfully. Redirecting to login...'
        
        // Redirect to login after successful reset
        setTimeout(() => {
            router.push('/login')
        }, 3000)

    } catch (err) {
        console.error('Error resetting password:', err)
        if (err.response && err.response.data) {
            // Handle Django validation errors (e.g., password too weak, token invalid)
            const data = err.response.data
            error.value = Object.values(data).flat().join(' ') || 'Password reset failed. The link may be invalid or expired.'
        } else {
            error.value = 'Password reset failed. Please try again.'
        }
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="auth-container">
        <div class="auth-card">
            <div class="header">
                <h1>Set New Password</h1>
                <p v-if="uidb64 && token">Enter your new password below.</p>
                <p v-else class="error-message">Invalid or missing reset token.</p>
            </div>

            <form v-if="uidb64 && token" @submit.prevent="handleReset" class="auth-form">
                <div class="input-group">
                    <label for="password">New Password</label>
                    <input 
                        type="password" 
                        id="password" 
                        v-model="newPassword1" 
                        placeholder="Enter new password"
                        required 
                    />
                </div>

                <div class="input-group">
                    <label for="confirm-password">Confirm New Password</label>
                    <input 
                        type="password" 
                        id="confirm-password" 
                        v-model="newPassword2" 
                        placeholder="Confirm new password"
                        required 
                    />
                </div>

                <button type="submit" class="submit-btn" :disabled="loading">
                    {{ loading ? 'Updating...' : 'Set Password' }}
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