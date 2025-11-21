<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import ExpenseForm from '@/components/ExpenseForm.vue'

const authStore = useAuthStore()
const expenses = ref([])
const loading = ref(false)
const showForm = ref(false)

const expenseToEdit = ref('')

const openAddModal = () => {
    expenseToEdit.value = null // Clear for Add Mode
    showForm.value = true
}

const openEditModal = (expense) => {
    expenseToEdit.value = expense
    showForm.value = true
}

const onExpenseSaved = () => {
    showForm.value = false
    fetchExpenses()
}

onMounted(async () => {
    await fetchExpenses()
})

const fetchExpenses = async () => {
    loading.value = true
    try {
        const response = await axios.get('http://192.168.100.40:8000/api/expenses/', {
            headers: {
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

const deleteExepense = async (id) => {
    if (!confirm('Are you sure you want to delete this expense?')) return

    try {
        await axios.delete(`http://192.168.100.40:8000/api/expenses/${id}/`, {
            headers: {
                Authorization: `Bearer ${authStore.token}`
            }
        })

        await fetchExpenses()
    } catch(error) {
        console.error("Error deleting expense: ", error)
        alert("Failed to delete expense.")
    }
}
</script>

<template>
    
    <div class="dashboard">
        <h2>My Expenses</h2>

        <button class="fab" @click="openAddModal">
            + Add
        </button>

        <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
            <div class="modal-content">
                <button class="close-btn" @click="showForm = false">&times;</button>

                <ExpenseForm :expense="expenseToEdit" @saved="onExpenseSaved" />
            </div>
        </div>

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
                <div class="expense-actions">
                    <span class="expense-amount">RM {{ expense.amount }}</span>
                    <button @click="openEditModal(expense)" class="icon-btn edit-btn">✎</button>
                    <button @click="deleteExepense(expense.id)" class="icon-btn delete-btn">&times;</button>
                </div>      
            </li>
        </ul>
    </div>
</template>

<style scoped>
.dashboard {
    padding-bottom: 80px;
    position: relative;
    min-height: 100%;
}

h2 {
    margin-bottom: 20px;
    text-align: center;
}

/* --- Floating Action Button (FAB) --- */
.fab {
    position: fixed;
    bottom: 80px;
    right: 20px;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 50px;
    padding: 15px 25px;
    font-size: 1rem;
    font-weight: bold;
    box-shadow: 0 4px 10px rgba(66, 185, 131, 0.4);
    cursor: pointer;
    z-index: 100;
    transition: transfrom 0.2s;
}

.fab:active{
    transform: scale(0.95);
}

/* --- Action --- */
.expense-actions {
    display: flex;
    align-items: center;
    gap: 15px;
}

/* Style Button */
.icon-btn {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    border: none;
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1;
}

.edit-btn {
    background-color: #eea838;
    margin-right: 5px;
    font-size: 1rem;
}

.edit-btn:hover {
    background-color: #f39c12;
}

.delete-btn {
    background-color: #ff4d4d;
}

.delete-btn:hover {
    background-color: #cc0000;
}

/* --- Model Styles --- */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7); /* Dark semi-transparent background */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000; /* Very high z-index to sit on top of everything */
    backdrop-filter: blur(3px); /* Nice blur effect */
}

.modal-content {
    position: relative;
    width: 90%;
    max-width: 400px;
    animation: slideUp 0.3s ease-out;
}

/* Simple animation to make the modal slide up */
@keyframes slideUp {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.close-btn {
    position: absolute;
    top: -10px;
    right: -10px;
    background: #ff4d4d;
    color: white;
    border: none;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    font-size: 1.2rem;
    cursor: pointer;
    z-index: 1001;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* --- Lists Styles --- */
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