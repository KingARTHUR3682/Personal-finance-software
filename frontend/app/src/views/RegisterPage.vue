<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const email = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)

const handleRegister = async () => {
    loading.value = true
    errorMessage.value = ''

    try {
        await axios.post('http://192.168.100.40:8000/api/register/', {
            username: username.value,
            email: email.value,
            password: password.value
        })

        alert('Account created successfully! Please log in.')
        router.push('/login')
    } catch (error) {
        console.error("Error registering:", error)
        if (error.response && error.response.data) {
            // Handle Django error object
            const data = error.response.data
            // Join array errors if they exist
            errorMessage.value = Object.values(data).flat().join(' ')
        } else {
            errorMessage.value = 'Registration failed. Please try again.'
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
                <h1>Create Account</h1>
                <p>Join us to track your finances</p>
            </div>

            <form @submit.prevent="handleRegister" class="auth-form">
                <div class="input-group">
                    <label>Username</label>
                    <input 
                        type="text" 
                        v-model="username" 
                        placeholder="Choose a username"
                        required 
                    />
                </div>
                
                <div class="input-group">
                    <label>Email</label>
                    <input 
                        type="email" 
                        v-model="email" 
                        placeholder="Enter your email"
                        required 
                    />
                </div>

                <div class="input-group">
                    <label>Password</label>
                    <input 
                        type="password" 
                        v-model="password" 
                        placeholder="Create a password"
                        required 
                    />
                </div>
                
                <button type="submit" class="submit-btn" :disabled="loading">
                    {{ loading ? 'Creating Account...' : 'Sign Up' }}
                </button>

                <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
            </form>

            <div class="footer">
                <p>Already have an account?</p>
                <router-link to="/login" class="link">Log In</router-link>
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
    border-color: #42b983; /* Green accent for Register */
    box-shadow: 0 0 0 3px rgba(66, 185, 131, 0.1);
}

.submit-btn {
    margin-top: 10px;
    padding: 16px;
    background-color: #42b983; /* Green button */
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: background-color 0.2s;
}

.submit-btn:hover {
    background-color: #3aa876;
}

.submit-btn:disabled {
    background-color: #a0dcc3;
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
    color: #42b983;
    font-weight: 600;
    text-decoration: none;
    margin-left: 5px;
}

.footer .link:hover {
    text-decoration: underline;
}
</style>