<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ExpenseForm from '@/components/ExpenseForm.vue'

const authStore = useAuthStore()
const router = useRouter()
const expenses = ref([])
const loading = ref(false)
const showForm = ref(false)
const filterType = ref('month') // 'day', 'week', 'month', 'custom'

const fetchExpenses = async () => {
    loading.value = true
    try {
        const response = await axios.get('http://192.168.100.40:8000/api/expenses/', {
            headers: { Authorization: `Bearer ${authStore.token}` }
        })
        expenses.value = response.data
    } catch(error) {
        console.error(error)
    } finally {
        loading.value = false
    }
}

onMounted(fetchExpenses)

// --- Filter Logic ---
const filteredList = computed(() => {
    const now = new Date()
    return expenses.value.filter(exp => {
        const expDate = new Date(exp.date)
        if (filterType.value === 'day') {
            return expDate.toDateString() === now.toDateString()
        } else if (filterType.value === 'month') {
            return expDate.getMonth() === now.getMonth() && expDate.getFullYear() === now.getFullYear()
        }
        // Add week logic here if needed
        return true 
    }).sort((a, b) => new Date(b.date) - new Date(a.date)) // Sort Newest First
})

// --- Totals Logic ---
const totalIncome = computed(() => 
    filteredList.value.filter(e => e.transaction_type === 'income')
    .reduce((sum, e) => sum + parseFloat(e.amount), 0).toFixed(2)
)

const totalExpense = computed(() => 
    filteredList.value.filter(e => e.transaction_type === 'expense')
    .reduce((sum, e) => sum + parseFloat(e.amount), 0).toFixed(2)
)

const balance = computed(() => (totalIncome.value - totalExpense.value).toFixed(2))

// --- Grouping Logic (Date Headers) ---
const groupedExpenses = computed(() => {
    const groups = {}
    filteredList.value.forEach(exp => {
        const dateKey = exp.date
        if (!groups[dateKey]) {
            groups[dateKey] = { date: dateKey, items: [], dayTotal: 0 }
        }
        groups[dateKey].items.push(exp)
        
        // Calculate daily impact
        const amt = parseFloat(exp.amount)
        if (exp.transaction_type === 'expense') groups[dateKey].dayTotal -= amt
        else groups[dateKey].dayTotal += amt
    })
    return Object.values(groups) // Convert object to array
})

// --- Navigation ---
const goToDetail = (id) => {
    router.push(`/expense/${id}`)
}
</script>

<template>
    <div class="dashboard">
        <div class="top-section">
            <div class="filter-bar">
                <span 
                    v-for="type in ['day', 'week', 'month', 'custom']" 
                    :key="type"
                    class="filter-item"
                    :class="{ active: filterType === type }"
                    @click="filterType = type"
                >
                    {{ type === 'custom' ? 'Custom' : type.charAt(0).toUpperCase() + type.slice(1) }}
                </span>
            </div>

            <div class="summary-container">
                <div class="balance-header">
                    <span class="label">Balance: RM {{ balance }}</span>
                </div>

                <div class="cards-row">
                    <div class="card expense-card">
                        <span class="card-label">Expense</span>
                        <span class="card-amount">RM {{ totalExpense }}</span>
                    </div>
                    <div class="card income-card">
                        <span class="card-label">Income</span>
                        <span class="card-amount">RM {{ totalIncome }}</span>
                    </div>
                </div>
            </div>
        </div>

        <button class="fab" @click="showForm = true">+</button>

        <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
            <div class="modal-content">
                <button class="close-btn" @click="showForm = false">&times;</button>
                <ExpenseForm @saved="() => { showForm = false; fetchExpenses() }" />
            </div>
        </div>

        <div class="history-section">
            <div class="list-header">
                <h4>Transactions</h4>
            </div>

            <div v-for="group in groupedExpenses" :key="group.date" class="date-group">
                <div class="date-header">
                    <span class="date-text">{{ group.date }}</span>
                    <span class="daily-total" :class="group.dayTotal < 0 ? 'red' : 'green'">
                        {{ group.dayTotal < 0 ? '-' : '+' }}RM {{ Math.abs(group.dayTotal).toFixed(2) }}
                    </span>
                </div>

                <div 
                    v-for="item in group.items" 
                    :key="item.id" 
                    class="transaction-item"
                    @click="goToDetail(item.id)"
                >
                    <div class="left-col">
                        <div class="icon-circle">{{ item.category_icon || 'QA' }}</div>
                        <div class="text-info">
                            <span class="item-name">{{ item.category_name || 'General' }}</span>
                            <span class="item-note">{{ item.description }}</span>
                        </div>
                    </div>
                    <div class="right-col">
                        <span class="item-amount" :class="item.transaction_type">
                            {{ item.transaction_type === 'expense' ? '-' : '' }}RM {{ item.amount }}
                        </span>
                    </div>
                </div>
            </div>
            
            <div v-if="filteredList.length === 0" class="empty-state">No records found.</div>
        </div>
    </div>
</template>

<style scoped>
/* General Layout */
.dashboard { background-color: #f5f5f5; min-height: 100vh; }

/* Top Section */
.top-section { background-color: white; padding: 15px 20px 25px; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }

/* Filters */
.filter-bar { display: flex; justify-content: space-between; margin-bottom: 20px; background: #f0f0f0; padding: 4px; border-radius: 10px; }
.filter-item { flex: 1; text-align: center; padding: 8px 0; font-size: 0.9rem; color: #888; border-radius: 8px; cursor: pointer; }
.filter-item.active { background: white; color: black; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }

/* Cards */
.balance-header { text-align: center; margin-bottom: 15px; font-weight: bold; color: #4991de; }
.cards-row { display: flex; gap: 15px; }
.card { flex: 1; padding: 15px; border-radius: 15px; color: white; display: flex; flex-direction: column; justify-content: center; }
.expense-card { background-color: #ff4d4d; }
.income-card { background-color: #42b983; }
.card-label { font-size: 0.85rem; opacity: 0.9; }
.card-amount { font-size: 1.2rem; font-weight: bold; margin-top: 5px; }

/* History Lists */
.history-section { padding: 20px; }
.list-header { display: flex; justify-content: space-between; margin-bottom: 10px; font-weight: bold; color: #333; }

.date-header { display: flex; justify-content: space-between; font-size: 0.85rem; color: #888; margin: 15px 0 5px; padding: 0 5px; }
.daily-total.red { color: #ff4d4d; }
.daily-total.green { color: #42b983; }

.transaction-item { background: white; padding: 12px 15px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; cursor: pointer; }
.left-col { display: flex; align-items: center; gap: 12px; }
.icon-circle { width: 40px; height: 40px; background: #f5f5f5; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
.text-info { display: flex; flex-direction: column; }
.item-name { font-weight: bold; font-size: 0.95rem; color: #333; }
.item-note { font-size: 0.75rem; color: #aaa; }
.item-amount { font-weight: bold; font-size: 1rem; }
.item-amount.expense { color: #333; } /* Usually standard color in modern apps, or red if preferred */
.item-amount.income { color: #42b983; }

/* FAB */
.fab { position: fixed; bottom: 90px; right: 20px; width: 50px; height: 50px; background: #eea838; color: white; border: none; border-radius: 50%; font-size: 1.5rem; box-shadow: 0 4px 12px rgba(238, 168, 56, 0.4); cursor: pointer; z-index: 100; }

/* Reuse your existing Modal CSS here... */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 2000; display: flex; align-items: center; justify-content: center; }
.modal-content { background: #2c2c2e; width: 90%; max-width: 400px; padding: 20px; border-radius: 20px; position: relative; }
.close-btn { position: absolute; top: 10px; right: 10px; background: red; color: white; border:none; width: 25px; height: 25px; border-radius: 50%; cursor: pointer;}
</style>