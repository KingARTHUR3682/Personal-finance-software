<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const expense = ref(null)
const loading = ref(true)

// Fetch specific expense data
onMounted(async () => {
  const id = route.params.id
  try {
    const response = await axios.get(`http://192.168.100.40:8000/api/expenses/${id}/`, {
      headers: { Authorization: `Bearer ${authStore.token}` }
    })
    expense.value = response.data
  } catch (error) {
    alert("Failed to fetch record details.")
    console.error("Error fetching record details: ", error)
    router.push('/')
  } finally {
    loading.value = false
  }
})

const deleteExpense = async () => {
  if (!confirm("Delete this record?")) return
  try {
    await axios.delete(`http://192.168.100.40:8000/api/expenses/${expense.value.id}/`, {
      headers: { Authorization: `Bearer ${authStore.token}` }
    })
    router.push('/')
  } catch (error) {
    alert("Failed to delete record")
    console.error("Error deleting record: ", error)
  }
}

const goBack = () => router.push('/')
</script>

<template>
  <div class="detail-page" v-if="expense">
    <div class="header">
      <button @click="goBack" class="back-btn">&lt;</button>
      <h3>Details</h3>
      <div style="width: 20px"></div> </div>

    <div class="content">
      <div class="main-info">
        <div class="big-icon">{{ expense.category_icon || 'qa' }}</div>
        <h4 class="cat-name">{{ expense.category_name || 'General' }}</h4>
        <h1 class="amount" :class="expense.transaction_type">
          {{ expense.transaction_type === 'income' ? '+' : '-' }} RM {{ expense.amount }}
        </h1>
      </div>

      <div class="detail-list">
        <div class="row">
          <span class="label">Type</span>
          <span>{{ expense.transaction_type }}</span>
        </div>
        <div class="row">
          <span class="label">Date</span>
          <span>{{ expense.date }}</span>
        </div>
        <div class="row">
          <span class="label">Note</span>
          <span>{{ expense.description || '-' }}</span>
        </div>
      </div>

      <div v-if="expense.receipt" class="receipt-container">
        <img :src="expense.receipt" alt="Receipt" />
      </div>

      <div class="actions">
        <button class="action-btn edit">Edit</button>
        <button class="action-btn delete" @click="deleteExpense">Delete</button>
      </div>
    </div>
  </div>
  <div v-else-if="loading" class="loading">Loading...</div>
</template>

<style scoped>
.detail-page { background: white; min-height: 100vh; display: flex; flex-direction: column; }
.header { display: flex; align-items: center; justify-content: space-between; padding: 15px; background: #f9f9f9; }
.back-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; }
.content { padding: 20px; display: flex; flex-direction: column; gap: 20px; }

.main-info { text-align: center; margin-bottom: 20px; }
.big-icon { font-size: 3rem; margin-bottom: 10px; }
.amount { font-size: 2rem; font-weight: bold; }
.amount.expense { color: #ff4d4d; }
.amount.income { color: #42b983; }

.detail-list { background: #f5f5f5; border-radius: 12px; padding: 15px; }
.row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }
.row:last-child { border-bottom: none; }
.label { color: #888; }

.receipt-container img { width: 100%; border-radius: 12px; margin-top: 10px; }

.actions { display: flex; gap: 15px; margin-top: auto; padding-top: 20px; }
.action-btn { flex: 1; padding: 15px; border: none; border-radius: 30px; font-weight: bold; cursor: pointer; font-size: 1rem; }
.edit { background: #eee; color: #333; }
.delete { background: #ff4d4d; color: white; }
</style>