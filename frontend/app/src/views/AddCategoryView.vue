<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// Form Fields
const name = ref('')
const icon = ref('🛒') // Default icon
const type = ref('expense')
const selectedParent = ref('') // Empty string means "Main Category" (parent = null)

// Data
const categories = ref([])

// Fetch all categories to populate the Parent dropdown
onMounted(async () => {
  try {
    const res = await axios.get('http://192.168.100.40:8000/api/categories/', {
        headers: { Authorization: `Bearer ${authStore.token}` }
    })
    categories.value = res.data
  } catch (error) {
    console.error("Error fetching categories", error)
  }
})

// Filter logic: Only show Main categories (parent=null) that match the selected Type
const parentOptions = computed(() => {
  return categories.value.filter(c => !c.parent && c.type === type.value)
})

const saveCategory = async () => {
  try {
    const payload = {
      name: name.value,
      icon: icon.value,
      type: type.value,
      // If selectedParent is empty, send null (creates a Main Category)
      parent: selectedParent.value || null 
    }

    await axios.post('http://192.168.100.40:8000/api/categories/', payload, {
      headers: { Authorization: `Bearer ${authStore.token}` }
    })
    router.push('/') // Go back to dashboard
  } catch (error) {
    alert('Failed to add category')
    console.error("Error adding category: ", error)
  }
}
</script>

<template>
  <div class="add-cat-page">
    <div class="header">
      <button @click="router.back()" class="cancel-btn">Cancel</button>
      <h3>New Category</h3>
      <button @click="saveCategory" class="save-btn">Save</button>
    </div>
    
    <div class="form-area">
      
      <div class="input-group">
        <label>Type</label>
        <div class="type-switcher">
            <button 
                :class="{ active: type === 'expense' }" 
                @click="type = 'expense'; selectedParent = ''"
            >
                Expense
            </button>
            <button 
                :class="{ active: type === 'income' }" 
                @click="type = 'income'; selectedParent = ''"
            >
                Income
            </button>
        </div>
      </div>

      <div class="input-group">
        <label>Parent Category</label>
        <select v-model="selectedParent">
          <option value="">Main Category (No Parent)</option>
          <option v-for="cat in parentOptions" :key="cat.id" :value="cat.id">
             {{ cat.icon }} {{ cat.name }}
          </option>
        </select>
      </div>

      <div class="input-group">
        <label>Name</label>
        <input v-model="name" placeholder="e.g., Coffee" />
      </div>

      <div class="input-group">
        <label>Icon (Emoji)</label>
        <input v-model="icon" placeholder="e.g., ☕" />
      </div>

    </div>
  </div>
</template>

<style scoped>
.add-cat-page { padding: 20px; background: #f5f5f5; min-height: 100vh; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.save-btn { color: #42b983; font-weight: bold; border: none; background: none; font-size: 1rem; cursor: pointer;}
.cancel-btn { color: #666; border: none; background: none; font-size: 1rem; cursor: pointer;}

.form-area { display: flex; flex-direction: column; gap: 15px; }

.input-group { background: white; padding: 15px; border-radius: 10px; }
.input-group label { display: block; margin-bottom: 8px; color: #888; font-size: 0.8rem; font-weight: bold; }
.input-group input, .input-group select { width: 100%; border: none; font-size: 1.1rem; outline: none; background: white; }

/* Type Switcher Styling */
.type-switcher { display: flex; background: #eee; padding: 4px; border-radius: 8px; }
.type-switcher button {
    flex: 1; border: none; background: transparent; padding: 8px; border-radius: 6px; cursor: pointer; font-weight: bold; color: #666;
}
.type-switcher button.active { background: white; color: #333; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
</style>