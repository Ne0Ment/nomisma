<script setup>
import { ref, onMounted } from 'vue';
import ConstYearDisplay from './ConstYearDisplay.vue';

const emit = defineEmits(['set-count']);

const props = defineProps({
    displayData: Object
});

function SetCount(d) {
    emit('set-count', d);
}
</script>

<template>
    <div class="flex flex-col w-full h-full overflow-auto">
        <ConstYearDisplay v-for="(data, year) in displayData" :year="year" :data="data" @set-count="SetCount"/>
    </div>
</template>