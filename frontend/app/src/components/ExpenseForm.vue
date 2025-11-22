<script setup>
import axios from 'axios';
import { ref, watch } from 'vue';
import { useAuthStore } from '@/stores/auth';
import CategoryGrid from './CategoryGrid.vue';

const props = defineProps({
  expense: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['expense-added'])

const authStore = useAuthStore()
const loading = ref(false)
const errorMessage = ref('')

const resetForm = () => {
    transactionType.value = 'expense'
    selectedCategoryId.value = null
    description.value = ''
    amount.value = ''
    date.value = new Date().toISOString().split('T')[0]
}

// --- Form Data ---
const transactionType = ref('expense')
const selectedCategoryId = ref(null)
const description = ref('')
const amount = ref('')
const date = ref(new Date().toISOString().split('T')[0]) // Default to today

watch(() => props.expense, (newExpense) => {
  if (newExpense) {
    // Edit mode: Fill the form
    transactionType.value = newExpense.transaction_type
    selectedCategoryId.value = newExpense.category
    description.value = newExpense.description
    amount.value = newExpense.amount
    date.value = newExpense.date
  } else {
    // Create mode: Clear the form
    resetForm()
  }
}, {immediate: true})


const handleSubmit = async () => {
  if (!selectedCategoryId.value) {
    errorMessage.value = "Please select a category."
    return
  }

  loading.value = true
  errorMessage.value = ''
  try {
      const headers = {Authorization: `Bearer ${authStore.token}`}
      const data = {
        transaction_type: transactionType.value,
        category: selectedCategoryId.value,
        description: description.value,
        amount: amount.value,
        date: date.value
      }

      if (props.expense) {
        // --- Edit mode (PUT) ---
        // Use the ID from prop
        await axios.put(`http://192.168.100.40:8000/api/expenses/${props.expense.id}/`, data, { headers })
      } else {
        // --- Create mode (POST) ---
        await axios.post('http://192.168.100.40:8000/api/expenses/', data, { headers })
      }

      resetForm()
      emit('saved')

  } catch(error) {
    console.error("Error saving: ", error)
    errorMessage.value = "Failed to save. Check your connection."
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="expense-form-card">
    
    <div class="type-switcher">
        <button 
            :class="{ active: transactionType === 'expense' }" 
            @click="transactionType = 'expense'"
        >
            Expense
        </button>
        <button 
            :class="{ active: transactionType === 'income' }" 
            @click="transactionType = 'income'"
        >
            Income
        </button>
    </div>

    <CategoryGrid 
        v-model="selectedCategoryId" 
        :transaction-type="transactionType" 
    />

    <form @submit.prevent="handleSubmit" class="form-layout">
      
      <div class="form-row">
        <div class="form-group">
          <label>Amount</label>
          <input v-model="amount" type="number" step="0.01" placeholder="0.00" required />
        </div>
        <div class="form-group">
          <label>Date</label>
          <input v-model="date" type="date" required />
        </div>
      </div>

      <div class="form-group">
        <label>Note / Description</label>
        <input v-model="description" type="text" placeholder="What was this for?" />
      </div>

      <button class="save-btn" type="submit" :disabled="loading">
        {{ loading ? 'Saving...' : 'Save Transaction' }}
      </button>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<style scoped>
.expense-form-card {
  background: #1c1c1e;
  padding: 20px;
  border-radius: 20px;
  /* Allow the modal to scroll if content is tall */
  max-height: 80vh; 
  overflow-y: auto;
}

/* Type Switcher Styles */
.type-switcher {
    display: flex;
    background: #2c2c2e;
    border-radius: 10px;
    padding: 4px;
    margin-bottom: 15px;
}
.type-switcher button {
    flex: 1;
    background: transparent;
    border: none;
    color: #888;
    padding: 8px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.2s;
}
.type-switcher button.active {
    background: #42b983; /* Or #ff4d4d for expense if you prefer */
    color: white;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

/* Form Layout */
.form-layout {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 10px;
}
.form-row {
  display: flex;
  gap: 15px;
}
.form-group {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}
label {
  font-size: 0.85rem;
  color: #aaa;
  margin-bottom: 5px;
}
input {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #333;
  background: #2c2c2e;
  color: white;
  font-size: 1rem;
}
.save-btn {
  margin-top: 10px;
  padding: 14px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
}
.save-btn:disabled {
  background-color: #555;
}
.error {
  color: #ff4d4d;
  font-size: 0.9rem;
  text-align: center;
}
</style>