<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const props = defineProps({ expense: { type: Object, default: null } })
const emit = defineEmits(['saved', 'close']) // Add 'close' emit
const router = useRouter()
const authStore = useAuthStore()

const picker = ref(null)

const openPicker = () => {
    picker.value.showPicker()
}

// --- Data ---
const categories = ref([])
const transactionType = ref('expense') 
const selectedParentId = ref(null)
const selectedCategory = ref(null)

// Form Data
const amountStr = ref('0') 
const description = ref('')
const date = ref(new Date().toISOString().split('T')[0])
const receiptFile = ref(null)
const fileInput = ref(null)

const dateLabel = computed(() => {
    const today = new Date().toISOString().split('T')[0]
    if (date.value === today) return 'Today'

    return date.value
})

// --- Loading Data ---
onMounted(async () => {
    try {
        const res = await axios.get(`${import.meta.env.VITE_API_URL}/api/categories/`, {
            headers: { Authorization: `Bearer ${authStore.token}` }
        })
        categories.value = res.data
        const firstParent = groupedCategories.value[0]
        if (firstParent) selectedParentId.value = firstParent.id
    } catch (error) { 
      console.error("Error fetching records: ", error) 
    }
})

// --- Computed Logic ---
const filteredCategories = computed(() => categories.value.filter(c => c.type === transactionType.value))

const groupedCategories = computed(() => {
    const parents = filteredCategories.value.filter(c => !c.parent)
    return parents.map(p => ({
        ...p,
        children: filteredCategories.value.filter(c => c.parent === p.id)
    }))
})

const currentChildren = computed(() => {
    if (!selectedParentId.value) return []
    const parent = groupedCategories.value.find(p => p.id === selectedParentId.value)
    return parent ? parent.children : []
})

// --- Keypad Logic ---
const onNumClick = (num) => {
    if (amountStr.value === '0' && num !== '.') amountStr.value = num.toString()
    else if (num === '.' && amountStr.value.includes('.')) return
    else amountStr.value += num.toString()
}

const onBackspace = () => {
    if (amountStr.value.length <= 1) amountStr.value = '0'
    else amountStr.value = amountStr.value.slice(0, -1)
}

const triggerFileUpload = () => fileInput.value.click()
const onFileChange = (e) => receiptFile.value = e.target.files[0]

// --- Submission ---
const handleSubmit = async () => {
    if (!selectedCategory.value) return alert("Please select a category")
    if (parseFloat(amountStr.value) === 0) return alert("Enter an amount")

    const formData = new FormData()
    formData.append('transaction_type', transactionType.value)
    formData.append('category', selectedCategory.value.id)
    formData.append('amount', amountStr.value)
    formData.append('description', description.value)
    formData.append('date', date.value)
    if (receiptFile.value) formData.append('receipt', receiptFile.value)

    try {
        const url = `${import.meta.env.VITE_API_URL}/api/expenses/`
        const config = { headers: { Authorization: `Bearer ${authStore.token}` }}
        
        if (props.expense) await axios.put(`${url}${props.expense.id}/`, formData, config)
        else await axios.post(url, formData, config)
        
        emit('saved')
    } catch (error) {
        alert("Failed to save record.")
        console.error("Error saving record: ", error)
    }
}

const goToAddCategory = () => router.push('/category/add')

</script>

<template>
<div class="page-layout">
    
    <div class="type-toggle">
        <span :class="{active: transactionType==='expense'}" @click="transactionType='expense'">Expense</span>
        <span :class="{active: transactionType==='income'}" @click="transactionType='income'">Income</span>       
    </div>

    <div class="parent-tabs">
        <div 
            v-for="p in groupedCategories" :key="p.id"
            class="tab-item"
            :class="{active: selectedParentId === p.id}"
            @click="selectedParentId = p.id"
        >
            {{ p.name }}
        </div>
    </div>

    <div class="category-grid">
        <div 
            v-for="c in currentChildren" :key="c.id"
            class="grid-item"
            :class="{selected: selectedCategory?.id === c.id}"
            @click="selectedCategory = c"
        >
            <div class="circle-icon">{{ c.icon }}</div>
            <span class="cat-name">{{ c.name }}</span>
        </div>
        <div class="grid-item" @click="goToAddCategory">
            <div class="circle-icon dashed">+</div>
            <span class="cat-name">Add</span>
        </div>
    </div>

    <div class="bottom-controls">
        <div class="info-bar">
            <input v-model="description" placeholder="Click to add note..." class="note-input"/>
            <div class="amount-display">
                <span class="curr">RM</span>
                <span class="val">{{ amountStr }}</span>
            </div>
        </div>

        <div class="keypad-container">
            <div class="num-pad">
                <button @click="onNumClick(7)">7</button>
                <button @click="onNumClick(8)">8</button>
                <button @click="onNumClick(9)">9</button>
                <button @click="onNumClick(4)">4</button>
                <button @click="onNumClick(5)">5</button>
                <button @click="onNumClick(6)">6</button>
                <button @click="onNumClick(1)">1</button>
                <button @click="onNumClick(2)">2</button>
                <button @click="onNumClick(3)">3</button>
                <button @click="onNumClick('.')">.</button>
                <button @click="onNumClick(0)">0</button>
                <button @click="onBackspace" class="icon-btn">⌫</button>
            </div>
            <div class="action-pad">
                <button class="img-btn" @click="triggerFileUpload">
                    {{ receiptFile ? '📷' : '🖼️' }}
                </button>
                <input type="file" ref="fileInput" hidden @change="onFileChange" accept="image/*">
                <div class="date-btn-wrapper" @click="openPicker">
                    <button class="date-btn">{{ dateLabel }}</button>
                    
                    <input ref="picker" type="date" v-model="date" class="hidden-date" />
                </div>
                <button class="submit-btn" @click="handleSubmit">OK</button>
            </div>
        </div>
    </div>

</div>
</template>

<style scoped>
/* --- Layout --- */
.page-layout {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: #f8f9fa;
    font-family: sans-serif;
    overflow: hidden; 
}

/* --- 1. Top Bar --- */
.type-toggle {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 15px;
    position: relative;
    background: white;
}
.type-toggle span {
    margin: 0 15px;
    font-weight: bold;
    color: #999;
    cursor: pointer;
    position: relative;
    padding-bottom: 5px;
}
.type-toggle span.active { color: #333; }
.type-toggle span.active::after {
    content: ''; position: absolute; bottom: 0; left: 0; width: 100%; height: 3px; background: #333; border-radius: 2px;
}
.settings-icon {
    position: absolute; right: 20px; font-size: 1.2rem; cursor: pointer; margin: 0 !important;
}
.close-icon {
    position: absolute; left: 20px; font-size: 1.2rem; cursor: pointer; margin: 0 !important; color: #333;
}

/* --- 2. Parent Tabs --- */
.parent-tabs {
    display: flex; overflow-x: auto; background: white; padding: 5px 10px; border-bottom: 1px solid #eee; white-space: nowrap;
}
.tab-item { padding: 8px 16px; color: #666; font-size: 0.9rem; cursor: pointer; }
.tab-item.active { color: #333; font-weight: bold; background: #f0f0f0; border-radius: 20px; }

/* --- 3. Grid --- */
.category-grid {
    flex: 1; overflow-y: auto; display: grid; grid-template-columns: repeat(4, 1fr); align-content: start; gap: 15px; padding: 20px;
}
.grid-item { display: flex; flex-direction: column; align-items: center; cursor: pointer; }
.circle-icon { width: 50px; height: 50px; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin-bottom: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
.circle-icon.dashed { border: 2px dashed #ccc; color: #ccc; box-shadow: none; }
.grid-item.selected .circle-icon { background: #ffeaa7; border: 2px solid #fdcb6e; }
.cat-name { font-size: 0.75rem; color: #666; text-align: center; }

/* --- 4. Bottom Controls --- */
.bottom-controls { background: white; border-top: 1px solid #eee; }
.info-bar { display: flex; justify-content: space-between; align-items: center; padding: 10px 15px; background: #f9f9f9; }
.note-input { border: none; background: transparent; font-size: 0.9rem; outline: none; width: 60%; color: #666; }
.amount-display { font-weight: bold; font-size: 1.2rem; }
.amount-display .curr { font-size: 0.9rem; margin-right: 5px; }

.keypad-container { display: flex; height: 240px; }
.num-pad { flex: 3; display: grid; grid-template-columns: repeat(3, 1fr); border-right: 1px solid #f0f0f0; }
.num-pad button { background: white; border: 1px solid #f9f9f9; font-size: 1.5rem; font-weight: 500; color: #333; cursor: pointer; }
.num-pad button:active { background: #eee; }

.action-pad { flex: 1; display: flex; flex-direction: column; }
.action-pad > button, .date-btn-wrapper { flex: 1; width: 100%; border: none; display: flex; align-items: center; justify-content: center; cursor: pointer; font-weight: bold; }
.img-btn { background: white; font-size: 1.2rem; border-bottom: 1px solid #eee !important; }
.date-btn-wrapper { position: relative; background: #42b983; color: white; overflow: hidden; }
.date-btn { background: transparent; border: none; color: white; font-weight: bold; width: 100%; height: 100%; }
.hidden-date { position: absolute; opacity: 0; width: 100%; height: 100%; cursor: pointer; top: 0; left: 0; z-index: 10; }
.submit-btn { background: #4991de; color: white; flex: 1.5 !important; }
</style>