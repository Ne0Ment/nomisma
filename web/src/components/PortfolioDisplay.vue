<script setup>
import { ref, onMounted, computed, toRef, watch } from 'vue';

const emit = defineEmits(['UpdateBonds']);

const props = defineProps({
    portfolios: Array
});

const portfolios = toRef(props, 'portfolios');

const chosenBonds = computed(() => {
    let bonds = [];
    for (const portfolio of portfolios.value) {
        if (portfolio.active) {
            bonds.push(...portfolio.bonds);
        }
    }
    return bonds;
});

function EmitNewBonds() {
    emit('UpdateBonds', chosenBonds.value);
}

onMounted(() => {
    EmitNewBonds()
});

</script>

<template>
    <div class="flex flex-col gap-2 ml-2 min-w-max">
        <h1 class="text-lg">портфели</h1>
        <div class="flex flex-row px-2 py-1 bg-neutral-200 min-w-max" v-for="portfolio in portfolios" :key="portfolio.name">
            <input class="w-6 h-6 min-w-max" type="checkbox" id="checkbox" v-model="portfolio.active" @change="EmitNewBonds" />
            <button class="grow px-2 flex flex-row min-w-max">
                <p>{{ portfolio.name }}</p>
            </button>
        </div>
    </div>
</template>