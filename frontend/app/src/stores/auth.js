import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
// -- State --
    // Initialize state from local storage if it exists
    const token = ref(localStorage.getItem('access_token') || null)

// -- Getter --
    const isAuthenticated = ref(!!token.value) // !! converts the value to boolean

// -- Action --
    // Function to set a token when a user log in
    function setToken(newToken) {
        token.value = newToken
        isAuthenticated.value = true
        localStorage.setItem('access_token', newToken)
    }

    // Function to clear the token when a user log out
    function logout() {
        token.value = null
        isAuthenticated.value = false
        localStorage.removeItem('access_token')
    }

    return { token, isAuthenticated, setToken, logout }
})