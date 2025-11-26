<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useExpenseStore } from '@/stores/expenseStore'
import ExpenseForm from '@/components/ExpenseForm.vue'

const expenseStore = useExpenseStore()
const router = useRouter()
const expenses = computed(() => expenseStore.expenses)
const showForm = ref(false)

// --- 1. State for Date Navigation ---
const filterType = ref('month') // Default to month
const currentDate = ref(new Date()) // Tracks the currently selected date
const customStart = ref(new Date().toISOString().split('T')[0])
const customEnd = ref(new Date().toISOString().split('T')[0])

onMounted(() => {
    expenseStore.fetchInitialData()
})

// --- 2. Helper Functions for Date Ranges ---
const getStartOfWeek = (date) => {
    const d = new Date(date)
    const day = d.getDay() // 0 (Sun) to 6 (Sat)
    const diff = d.getDate() - day + (day === 0 ? -6 : 1) // Adjust to Monday start
    return new Date(d.setDate(diff))
}

const getEndOfWeek = (date) => {
    const d = getStartOfWeek(date)
    d.setDate(d.getDate() + 6)
    return d
}

// --- 3. Navigation Logic (< Prev | Next >) ---
const shiftDate = (step) => {
    const newDate = new Date(currentDate.value)
    if (filterType.value === 'day') {
        newDate.setDate(newDate.getDate() + step)
    } else if (filterType.value === 'week') {
        newDate.setDate(newDate.getDate() + (step * 7))
    } else if (filterType.value === 'month') {
        newDate.setMonth(newDate.getMonth() + step)
    }
    currentDate.value = newDate
}

// Display text for the current date range (e.g., "Nov 2025")
const dateDisplay = computed(() => {
    const opts = { year: 'numeric', month: 'short', day: 'numeric' }
    const d = currentDate.value
    
    if (filterType.value === 'day') return d.toLocaleDateString('en-MY', opts)
    if (filterType.value === 'month') return d.toLocaleDateString('en-MY', { month: 'long', year: 'numeric' })
    if (filterType.value === 'week') {
        const start = getStartOfWeek(d)
        const end = getEndOfWeek(d)
        return `${start.getDate()} ${start.toLocaleString('default', { month: 'short' })} - ${end.getDate()} ${end.toLocaleString('default', { month: 'short' })}`
    }
    return 'Custom Range'
})

// --- 4. Filter Logic ---
const filteredList = computed(() => {
    return expenses.value.filter(exp => {
        const expDate = new Date(exp.date)
        // Reset times for accurate comparison
        expDate.setHours(0,0,0,0)
        const curr = new Date(currentDate.value)
        curr.setHours(0,0,0,0)

        if (filterType.value === 'day') {
            return expDate.getTime() === curr.getTime()
        } 
        else if (filterType.value === 'week') {
            const start = getStartOfWeek(curr)
            const end = getEndOfWeek(curr)
            // Check if date is between start and end
            start.setHours(0,0,0,0)
            end.setHours(23,59,59,999)
            return expDate >= start && expDate <= end
        } 
        else if (filterType.value === 'month') {
            return expDate.getMonth() === curr.getMonth() && expDate.getFullYear() === curr.getFullYear()
        } 
        else if (filterType.value === 'custom') {
            const start = new Date(customStart.value)
            const end = new Date(customEnd.value)
            start.setHours(0,0,0,0)
            end.setHours(23,59,59,999)
            return expDate >= start && expDate <= end
        }
        return true 
    }).sort((a, b) => new Date(b.date) - new Date(a.date))
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

// --- Grouping Logic ---
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
    return Object.values(groups)
})

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
            
            <Transition name="fade" mode="out-in">
                <div class="date-nav" v-if="filterType !== 'custom'">
                    <button @click="shiftDate(-1)" class="nav-arrow">&lt;</button>
                    <span class="current-date-label">{{ dateDisplay }}</span>
                    <button @click="shiftDate(1)" class="nav-arrow">&gt;</button>
                </div>

                <div class="custom-inputs" v-else>
                    <input type="date" v-model="customStart">
                    <span>to</span>
                    <input type="date" v-model="customEnd">
                </div>
            </Transition>

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

        <Transition name="fade">
            <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
            <div class="modal-content">
                <ExpenseForm 
                    @saved="showForm = false" 
                    @close="showForm = false"
                />
            </div>
        </div>
        </Transition>

        <div class="history-section">
            <div class="list-header">
                <h4>Transactions</h4>
            </div>

            <TransitionGroup name="list" tag="div">
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
                            <span v-if="item.isPending" style="font-size:0.7rem; color:orange; display:block; text-align:right;">⏳</span>
                        </div>
                    </div>
                </div>
            </TransitionGroup>         
            
            <div v-if="filteredList.length === 0" class="empty-state">
                No records found for this period.
            </div>
        </div>
    </div>
</template>

<style scoped>
/* General Layout */
.dashboard { background-color: #f5f5f5; min-height: 100vh; }

/* Top Section */
.top-section { 
    background-color: white; 
    padding: 15px 20px 25px; 
    border-bottom-left-radius: 20px; 
    border-bottom-right-radius: 20px; 
    box-shadow: 0 2px 10px rgba(0,0,0,0.05); 
}

/* Filters */
.filter-bar { display: flex; justify-content: space-between; margin-bottom: 15px; background: #f0f0f0; padding: 4px; border-radius: 10px; }
.filter-item { flex: 1; text-align: center; padding: 8px 0; font-size: 0.9rem; color: #888; border-radius: 8px; cursor: pointer; transition: all 0.3s ease; } /* Smoother transition */
.filter-item.active { background: white; color: black; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.05); transform: scale(1.02); } /* Slight pop */

/* Date Navigation */
.date-nav { display: flex; justify-content: center; align-items: center; margin-bottom: 20px; gap: 15px; }
.nav-arrow { background: none; border: none; font-size: 1.5rem; color: #4991de; cursor: pointer; padding: 0 10px; font-weight: bold; transition: transform 0.1s; }
.nav-arrow:active { transform: scale(0.9); }
.current-date-label { font-weight: 600; font-size: 1rem; color: #333; min-width: 150px; text-align: center; }

/* Custom Inputs */
.custom-inputs { display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 20px; }
.custom-inputs input { padding: 5px; border: 1px solid #ddd; border-radius: 5px; }

/* Cards */
.balance-header { text-align: center; margin-bottom: 15px; font-weight: bold; color: #4991de; }
.cards-row { display: flex; gap: 15px; }
.card { flex: 1; padding: 15px; border-radius: 15px; color: white; display: flex; flex-direction: column; justify-content: center; }
.expense-card { background-color: #ff4d4d; }
.income-card { background-color: #42b983; }
.card-label { font-size: 0.85rem; opacity: 0.9; }
.card-amount { font-size: 1.2rem; font-weight: bold; margin-top: 5px; }

/* History Lists */
.history-section { padding: 20px; padding-bottom: 90px; } 
.list-header { display: flex; justify-content: space-between; margin-bottom: 10px; font-weight: bold; color: #333; }

.date-header { display: flex; justify-content: space-between; font-size: 0.85rem; color: #888; margin: 15px 0 5px; padding: 0 5px; }
.daily-total.red { color: #ff4d4d; }
.daily-total.green { color: #42b983; }

.transaction-item { background: white; padding: 12px 15px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; cursor: pointer; box-shadow: 0 1px 3px rgba(0,0,0,0.05); transition: transform 0.1s; }
.transaction-item:active { transform: scale(0.98); }

.left-col { display: flex; align-items: center; gap: 12px; }
.icon-circle { width: 40px; height: 40px; background: #f5f5f5; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; }
.text-info { display: flex; flex-direction: column; }
.item-name { font-weight: bold; font-size: 0.95rem; color: #333; }
.item-note { font-size: 0.75rem; color: #aaa; }
.item-amount { font-weight: bold; font-size: 1rem; }
.item-amount.expense { color: #333; }
.item-amount.income { color: #42b983; }

.empty-state { text-align: center; color: #aaa; margin-top: 30px; }

/* FAB */
.fab { position: fixed; bottom: 90px; right: 20px; width: 50px; height: 50px; background: #eea838; color: white; border: none; border-radius: 50%; font-size: 1.5rem; box-shadow: 0 4px 12px rgba(238, 168, 56, 0.4); cursor: pointer; z-index: 100; transition: transform 0.2s; }
.fab:active { transform: scale(0.9); }

/* Modal */
.modal-overlay { 
    position: fixed; 
    top: 0; 
    left: 0; 
    width: 100%; 
    height: 100%; 
    background: rgba(0,0,0,0.05); 
    z-index: 2000; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    backdrop-filter: blur(1px);
}

.modal-content { 
    background: #2c2c2e; 
    width: 95%; 
    max-width: 420px; 
    padding: 0; 
    border-radius: 20px; 
    position: relative;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    overflow: hidden;
}

/* --- ANIMATION STYLES --- */

/* Fade Transition (for Date Nav & Modal) */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}

/* List Transition (for Transactions) */
.list-move,
.list-enter-active,
.list-leave-active {
  transition: all 0.4s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* Ensure items leave smoothly without taking up space instantly */
.list-leave-active {
  position: absolute;
  width: 100%;
}
</style>