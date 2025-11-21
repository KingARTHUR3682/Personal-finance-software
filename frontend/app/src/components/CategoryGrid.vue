<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth';

// Props:
// - modelValue: The selected category ID (for v-model support)
// - transactionType: 'expense' or 'income' (to filter the list)
const props = defineProps(['modelValue', 'transactionType'])
const emit = defineEmits(['update:modelValue'])

const authStore = useAuthStore()
const categories = ref([])

onMounted(async () => {
    try {
        const response = await axios.get('http://192.168.100.40:8000/api/categories/', {
            headers: { Authorization: `Bearer ${authStore.token}` }
        })
        categories.value = response.data
    } catch(error) {
        console.error("Error loading categories: ", error)
    }
})

// 1. Filter by Type (Expense or Income)
const typeCategories = computed(() => {
    return categories.value.filter(c => c.type === props.transactionType)
})

// 2. Group by Parent
// This create structure like: [ { mainCategory, children: [subCategory, subCategory] }, ... ]
const groupedCategories = computed(() => {
    // Get all "Main" categories (parent = null)
    const parents = typeCategories.value.filter(c => !c.parent)

    return parents.map(parent => ({
        ...parent,
        // Find all "Sub" categories that belong top the "Main" parent
        children: typeCategories.value.filter(c => c.parent === parent.id)
    }))
})

const selectCategory = (category) => {
    emit('update:modelValue', category.id)
}
</script>

<template>
    <div class="category-grid">
        <div v-for="group in groupedCategories" :key="group.id" class="category-group">
            <h4 class="group-title">{{ group.icon }} {{ group.name }}</h4>

            <div class="grid">
                <div
                    v-for="child in group.children"
                    :key="child.id"
                    class="category-item"
                    :class="{ active: modelValue === child.id }"
                    @click="selectCategory(child)"
                >
                    <div class="icon">{{ child.icon }}</div>
                    <span class="name">{{ child.name }}</span>
                </div>
            </div>
        </div>
        <p v-if="groupedCategories.length === 0" class="empty-msg">
            No categories found for {{ transactionType }}.
        </p>
    </div>
</template>

<style scoped>
.category-grid {
  max-height: 300px;
  overflow-y: auto;
  padding: 10px 0;
}

.group-title {
  font-size: 0.9rem;
  color: #888;
  margin: 15px 0 8px 5px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 4 items per row */
  gap: 12px;
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #3a3a3c;
  border-radius: 12px;
  padding: 10px;
  cursor: pointer;
  aspect-ratio: 1; /* Keeps them square */
  transition: all 0.2s;
}

.category-item.active {
  background: #42b983;
  color: white;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(66, 185, 131, 0.4);
}

.icon {
  font-size: 1.8rem;
  margin-bottom: 5px;
}

.name {
  font-size: 0.75rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.empty-msg {
    text-align: center;
    color: #666;
    margin-top: 20px;
}
</style>