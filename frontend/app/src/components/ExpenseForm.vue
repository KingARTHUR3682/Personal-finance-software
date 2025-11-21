<script setup>
import axios from 'axios';
import { ref, watch } from 'vue';
import { useAuthStore } from '@/stores/auth';

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

const name = ref('')
const amount = ref('')
const date = ref('')

watch(() => props.expense, (newExpense) => {
  if (newExpense) {
    // Edit mode: Fill the form
    name.value = newExpense.name
    amount.value = newExpense.amount
    date.value = newExpense.date
  } else {
    // Create mode: Clear the form
    name.value = ''
    amount.value = ''
    date.value = ''
  }
}, {immediate: true})

const handleSubmit = async () => {
  loading.value = true
  errorMessage.value = ''
  try {
      const headers = {Authorization: `Bearer ${authStore.token}`}
      const data = {
        name: name.value,
        amount: amount.value,
        date: date.value
      }

      if (props.expense) {
        // --- Edit mode (PUT) ---
        // Use the ID from prop
        await axios.put(`http://192.168.100.39:8000/api/expenses/${props.expense.id}/`, data, { headers })
      } else {
        // --- Create mode (POST) ---
        await axios.post('http://192.168.100.39:8000/api/expenses/', data, { headers })
      }

      name.value = ''
      amount.value = ''
      date.value = ''
      emit('saved')
  } catch(error) {
    console.error("Error saving expense: ", error)
    errorMessage.value = "Failed to save expense."
  } finally {
    loading.value = false
  }
}
</script>

<template>
    <div class="expense-form-card">
    <h3>Add New Expense</h3>
    
    <form @submit.prevent="handleSubmit" class="form-layout">
      <div class="form-group">
        <label>Name</label>
        <input v-model="name" type="text" placeholder="e.g. Lunch" required />
      </div>

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

      <button type="submit" :disabled="loading">
        {{ loading ? 'Saving...' : (expense ? 'Update Expense' : 'Add Expense') }}
      </button>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<style scoped>
.expense-form-card {
  background: #2c2c2e;
  padding: 20px;
  border-radius: 15px;
  margin-bottom: 20px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}
h3 {
  margin-bottom: 15px;
  color: #fff;
}
.form-layout {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.form-row {
  display: flex;
  gap: 15px;
}
.form-group {
  display: flex;
  flex-direction: column;
  flex: 1;
}
label {
  font-size: 0.85rem;
  color: #aaa;
  margin-bottom: 5px;
}
input {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #444;
  background: #1c1c1e;
  color: white;
  font-size: 1rem;
  min-width: 0;
}
button {
  margin-top: 10px;
  padding: 12px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}
button:disabled {
  background-color: #555;
}
.error {
  color: #ff4d4d;
  font-size: 0.9rem;
  text-align: center;
}
</style>