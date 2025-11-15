import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
// -- State --
    const token = ref(null)

// -- Getter --
    const isAuthenticated = ref(!!token.value) // !! converts the value to boolean

// -- Action --
    // Function to set a token when a user log in
    function setToken(newToken) {
        token.value = newToken
        isAuthenticated.value = true
    }

    // Function to clear the token when a user log out
    function logout() {
        token.value = null
        isAuthenticated.value = false
    }

    return { token, isAuthenticated, setToken, logout }
})