<script setup>
import { ref } from 'vue'
const searchValue = ref('');

const emit = defineEmits(['UpdateSearch'])

function EmitSearch(t){
    emit('UpdateSearch', searchValue.value);
}
</script>

<template>
<input type="search" class="text-xl p-2 border-neutral-400 border-2 rounded-xl"
    @keyup.enter.native="EmitSearch" v-model="searchValue"/>
</template>