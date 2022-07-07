<script setup>
import BondDisplay from './BondDisplay.vue';

const props = defineProps({
    bonds: Array
});

</script>

<template>
    <div class="flex flex-col overflow-auto gap-2 mt-2">
        <BondDisplay v-for="bond of bonds" :key="bond.figi" :bond="bond" />
    </div>
</template>