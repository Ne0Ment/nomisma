<script setup>
import { ref, toRef, computed, onMounted, watch } from 'vue'
import { sort } from 'fast-sort';

import PortfolioDisplay from "./PortfolioDisplay.vue";
import CalcSettings from './CalcSettings.vue';
import DataDisplay from './DataDisplay.vue';
import PieAnalysis from './PieAnalysis.vue';
import PieSettings from './PieSettings.vue';
import TableAnalysis from './TableAnalysis.vue';
import TableFilters from './TableFilters.vue';
import { set } from '@vueuse/core';
import ConstructorPortfolios from './ConstructorPortfolios.vue';

const props = defineProps({
    portfolios: Array,
    allBonds: Array
});

const portfolios = toRef(props, 'portfolios');
const allBonds = ref(props.allBonds);
const filters = ref([]);

function FilterBonds() {
    console.log(filters.value)
    const f = allBonds.value.map(bond => {
        let newBond = { ...bond };
        let ok = true;
        if (filters.value) {
            for (const filter of Object.keys(filters.value)) {
                if (!filters.value[filter][bond[filter]]) {
                    ok = false;
                    break;
                }
            }
        }
        newBond.allowed = ok;
        return newBond;
    });
    console.log(f.filter(t => t.allowed));
    allBonds.value = f;
}

onMounted(() => {
    console.log(props)
})

const displayData = ref({});

const tab = ref(0);

function UpdateFilters(v) {
    filters.value = v;
    FilterBonds();
}

</script>

<template>
    <div class="flex flex-col overflow-hidden">
        <div class="flex flex-row gap-2 mt-2">
            <button class="hover:bg-neutral-600 hover:text-white rounded-md p-1"
                :class="tab == 0 ? 'active-tab' : 'passive-tab'" @click="tab = 0">
                календарь
            </button>
            <button class="hover:bg-neutral-600 hover:text-white rounded-md p-1"
                :class="tab == 1 ? 'active-tab' : 'passive-tab'" @click="tab = 1">
                анализ
            </button>
            <button class="hover:bg-neutral-600 hover:text-white rounded-md p-1"
                :class="tab == 2 ? 'active-tab' : 'passive-tab'" @click="tab = 2">
                список
            </button>
        </div>
        <div class="flex flex-row h-full mt-2 overflow-hidden gap-2">
            <div class="flex flex-col grow">
                <p v-for="bond of allBonds">{{ bond.ticker }}</p>
                <!-- <DataDisplay v-if="(tab == 0)" :display-data="displayData" /> -->
            </div>
            <div class="flex flex-col gap-4">
                <ConstructorPortfolios v-if="portfolios != []" :portfolios="portfolios" />
                <TableFilters :all-bonds="allBonds" @emit-filters="UpdateFilters" />
            </div>
        </div>
    </div>
</template>

<style>
.active-tab {
    @apply bg-neutral-600 text-white
}

.passive-tab {
    @apply bg-white text-black
}
</style>