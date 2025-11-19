<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const emit = defineEmits(['expense-added'])

const authStore = useAuthStore()
const loading = ref(false)
const errorMessage = ref('')

const name = ref('')
const amount = ref('')
const date = ref('')

const handleSubmit = async () => {
    loading.value = true
    errorMessage.value = ''
    try {
        await axios.post('http://192.168.100.40:8000/api/expenses/', {
            name: name.value,
            amount: amount.value,
            date: date.value
        }, {
            headers: {
                Authorization: `Bearer ${authStore.token}`
            }
        })

        // Clear the form
        name.value = ''
        amount.value = ''
        date.value = ''

        // Tell the parent components to refresh the list
        emit('expense-added')
    } catch(error) {
        console.error("Error adding expense: ", error)
        errorMessage.value = "Failed to add expense."
    } finally {
        loading.value = true
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
        {{ loading ? 'Adding...' : 'Add Expense' }}
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