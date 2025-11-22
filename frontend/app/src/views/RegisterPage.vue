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

        alert('Account created, please log in.')
        router.push('/login')
    } catch (error) {
        console.error("Error register new user: ", error)
        if (error.response && error.response.data) {
            // Show specific errors from Django. ("Username already exists.")
            errorMessage.value = JSON.stringify(error.response.data)
        } else {
            errorMessage.value = 'Registration failed.'
        }
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="auth-page">
        <h2>Create Account</h2>
        <form @submit.prevent="handleRegister">
            <div class="form-group">
                <label>Username</label>
                <input type="text" v-model="username" required />
            </div>
            
            <div class="form-group">
                <label>Email</label>
                <input type="email" v-model="email" required />
            </div>

            <div class="form-group">
                <label>Password</label>
                <input type="password" v-model="password" required />
            </div>
            
            <button type="submit" :disabled="loading">
                {{ loading ? 'Creating...' : 'Sign Up' }}
            </button>

            <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

            <p class="switch-link">
                Already have an account? <router-link to="/login">Log In</router-link>
            </p>
        </form>
    </div>
</template>

<style scoped>
/* Reusing styles similar to Login for consistency */
.auth-page {
    max-width: 400px;
    margin: 50px auto;
    padding: 20px;
}
.form-group { 
    margin-bottom: 15px;
}
label { 
    display: block; 
    margin-bottom: 5px; 
    color: #aaa; 
}
input { 
    width: 100%; padding: 10px; 
    border-radius: 8px; border: 1px solid #444;
    background: #2c2c2e; color: white;
}
button {
    width: 100%; padding: 12px;
    background-color: #42b983; color: white;
    border: none; border-radius: 8px;
    font-weight: bold; cursor: pointer;
    margin-top: 10px;
}
button:disabled { 
    background-color: #555; 
}
.error { 
    color: #ff4d4d; 
    font-size: 0.9rem; 
    margin-top: 10px; 
}
.switch-link { 
    text-align: center; 
    margin-top: 20px; 
    font-size: 0.9rem; 
    color: #aaa; 
}
.switch-link a { 
    color: #42b983; 
    text-decoration: none; 
}
</style>