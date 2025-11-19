<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const expenses = ref([])
const loading = ref(false)

onMounted(async () => {
    await fetchExpenses()
})

const fetchExpenses = async () => {
    loading.value = true
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/expenses/', {
            header: {
                Authorization: `Bearer ${authStore.token}`
            }
        })
        expenses.value = response.data

    } catch(error) {
        console.error("Error fetching expenses: ", error)
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="dashboard">
        <h2>My Expenses</h2>

        <div v-if="loading" class="loading">Loding...</div>

        <div v-else-if="expenses.length === 0" class="empty-state">
            <p>No expenses found</p>
            <p>Time to add one</p>
        </div>

        <ul v-else class="expense-list">
            <li v-for="expense in expenses" :key="expense.id" class="expense-item">
                <div class="expense-info">
                    <span class="expense-name">{{ expense.name }}</span>
                    <span class="expense-date">{{ expense.date }}</span>
                </div>
                <span class="expense-amount">RM {{ expense.amount }}</span>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.dashboard {
    padding-bottom: 60px
}

h2 {
    margin-bottom: 20px;
    text-align: center;
}

.expense-list {
    list-style: none;
    padding: 0;
}

.expense-item {
    background: #2c2c2e;
  color: white;
  margin-bottom: 10px;
  padding: 15px;
  border-radius: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.expense-info {
    display: flex;
    flex-direction: column;
}

.expense-name {
    font-weight: bold;
    font-size: 1.1rem;
}

.expense-date {
    font-size: 0.8rem;
    color: #aaa;
}

.expense-amount {
    font-weight: bold;
    color: #42b983;
    font-size: 1.2rem;
}

.empty-state {
    text-align: center;
    margin-top: 50px;
    color: #888;
}
</style>