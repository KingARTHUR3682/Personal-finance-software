import { defineStore } from "pinia"
import axios from 'axios'
import { useAuthStore } from "./auth"

export const useExpenseStore = defineStore('expenses', {
    state: () => ({
        expenses: [], // List of transactions
        categories: [], // Cache categories for offline
        pendingQueue: [], // List of waiting offline items
    }),

    actions: {
        // 1. Fetch data if online
        async fetchInitialData() {
            if (!navigator.onLine) return // Stop if offline

            const authStore = useAuthStore()
            try {
                // Fetch Categories
                const categoriesResponse = await axios.get(`${import.meta.env.VITE_API_URL}/api/categories/`, {
                    headers: { Authorization: `Bearer ${authStore.token}` }
                })
                this.categories = categoriesResponse.data

                // Fetch Expenses
                const expensesResponse = await axios.get(`${import.meta.env.VITE_API_URL}/api/expenses/`, {
                    headers: { Authorization: `Bearer ${authStore.token}` }
                })

                // Merge
                this.expenses = [
                    ...this.expenses.filter(e => e.isPending),
                    ...expensesResponse.data
                ]
            } catch(error) {
                console.error("Error syncing records, viewing local data only: ", error)
            }
        },

        // 2. Add expenses (Save locally first)
        async addExpense(expenseData, file = null) {
            const tempId = Date.now() // Ganerate a fake ID

            const newExpense = {
                id: tempId,
                ...expenseData,
                isPending: true, // Mark as "Not synced yet"
                date: expenseData.date || new Date().toISOString.split('T')[0]
            }

            this.expenses.unshift(newExpense)

            this.pendingQueue.push({
                tempId,
                data: expenseData,
                hasFile: !!file
            })

            this.processQueue()
        },

        async processQueue() {
            if (!navigator.onLine || this.pendingQueue.length === 0) return

            const authStore = useAuthStore()

            const queue = [...this.pendingQueue]

            for (const record of queue) {
                try {
                    const formData = new FormData()
                    for (const key in record.data) {
                        formData.append(key, record.data[key])
                    }

                    const response = await axios.post(
                        `${import.meta.env.VITE_API_URL}/api/expenses/`, 
                        formData, 
                        { headers: { Authorization: `Bearer ${authStore.token}` }}
                    )

                    // Remove from queue if success
                    this.pendingQueue = this.pendingQueue.filter(p => p.tempId !== record.tempId)

                    // Update the local list with the REAL data from server
                    const index = this.expenses.findIndex(e => e.id === record.tempId)
                    if (index !== -1) {
                        this.expenses[index] = response.data
                    }
                } catch(error) {
                    console.error("Error syncing record: ", record.tempId, ", error: ", error)
                    break // Stop uploading if server is down
                }
            }
        }
    },

    persist: true
})