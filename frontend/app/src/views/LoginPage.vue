<script setup>
import { ref } from 'vue'

// Create "reactive" variables for the from fields
const username = ref('')
const password = ref('')

// Function to handle the form submission
const handleLogin = () => {
    console.log('Logging in with:', username.value, password.value)
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
        </form>
    </div>
</template>

<style scoped>
.login-page {
    max-width: 400px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
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
</style>