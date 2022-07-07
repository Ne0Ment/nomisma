<script setup>
import { ref } from 'vue'
const searchValue = ref('');

const emit = defineEmits(['UpdateSearch'])
const timer = ref(undefined);

function EmitSearch(t){
    emit('UpdateSearch', searchValue.value);
}

function TextSearch() {
    clearTimeout(timer.value);
    timer.value = setTimeout(() => {
        EmitSearch();
    }, 200);
}
</script>

<template>
<input type="search" class="text-xl p-2 border-neutral-600 border-2 rounded-xl mr-4 "
    @keydown="TextSearch" v-model="searchValue"/>
</template>