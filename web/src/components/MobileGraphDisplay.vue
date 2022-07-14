<script setup>
import { ref, onMounted } from 'vue';
import MobileYearDisplay from './MobileYearDisplay.vue';

const props = defineProps({
    displayData: Object
});

</script>

<template>
    <div class="flex flex-col grow h-full min-w-0">
        <div class="flex flex-col grow min-w-0 overflow-auto">
            <div v-for="(data, year) in displayData">
                <MobileYearDisplay :data="data" :year="year"/>
            </div>
        </div>
    </div>
</template>