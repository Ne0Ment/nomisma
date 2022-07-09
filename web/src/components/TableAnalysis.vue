<script setup>
import { computed, onMounted, ref, toRef, watch } from 'vue';
import BondDisplay from './searchcomponents/BondDisplay.vue';
import { sort } from 'fast-sort';


const props = defineProps({
    allBonds: Array,
    filters: Object,
    n: Number
});

const allBonds = toRef(props, 'allBonds');
const filters = toRef(props, 'filters');
const nn = toRef(props, 'n');
const bonds = ref([]);
const sorterFn = ref((bond) => bond.coupon_profitability);
const chosenSort = ref(3);
const reverseSort = ref(false);

function CalcBonds() {
    let figis = [];
    let a = [];
    if (allBonds.value) {
        for (const bond of allBonds.value) {
            let ok = true;
            if (filters.value) {
                for (const filter of Object.keys(filters.value)) {
                    if (!filters.value[filter][bond[filter]]) {
                        ok = false;
                        break;
                    }
                }
            }
            if (ok) {
                const bi = figis.indexOf(bond.figi);
                if (bi == -1) {
                    figis.push(bond.figi);
                    a.push({ ...bond });
                } else {
                    a[bi].count += bond.count;
                }
            }
        }
    }
    if (reverseSort.value) {
        a = sort(a).asc(sorterFn.value);
    } else {
        a = sort(a).desc(sorterFn.value);
    }
    bonds.value = a;
}

watch(filters, (o, n) => {
    CalcBonds();
});

watch(nn, (o, n) => {
    CalcBonds();
});

onMounted(() => {
    CalcBonds();
});

function SetSort(n) {
    if (chosenSort.value==n) {
        reverseSort.value = !reverseSort.value;
    } else {
        chosenSort.value = n;    
        reverseSort.value = false;
    }
    
    switch(n) {
        case 0:
            sorterFn.value = ((bond) => bond.count);
            break;
        case 1:
            sorterFn.value = ((bond) => (bond.count*bond.market_price));
            break;
        case 2:
            sorterFn.value = ((bond) => bond.market_price / bond.nominal)
            break;
        case 3:
            sorterFn.value = ((bond) => bond.profitability);
            break;
        case 4:
            sorterFn.value = ((bond) => bond.coupon_profitability);
            break;
    }
    CalcBonds();
}

</script>

<template>
    <div class="table-wrp block max-h-full overflow-auto">
        <table class="w-full overflow-auto">
            <thead class="bg-white sticky top-0 border-b">
                <tr>
                    <th>
                        <p>тикер</p>
                    </th>
                    <th>
                        <p>наименование</p>
                    </th>
                    <th @click="SetSort(0)" :class="chosenSort==0 ? 'active-sort' : ''">
                        <p>кол-во</p>
                    </th>
                    <th @click="SetSort(1)" :class="chosenSort==1 ? 'active-sort' : ''">
                        <p>сумма</p>
                    </th>
                    <th @click="SetSort(2)" :class="chosenSort==2 ? 'active-sort' : ''">
                        <p>% от номин</p>
                    </th>
                    <th @click="SetSort(3)" :class="chosenSort==3 ? 'active-sort' : ''">
                        <p>тек. доход.</p>
                    </th>
                    <th @click="SetSort(4)" :class="chosenSort==4 ? 'active-sort' : ''">
                        <p>дох. к погаш.</p>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="bond of bonds">
                    <td>
                        <p>{{ bond.ticker }}</p>
                    </td>
                    <td>
                        <p>{{ bond.name }}</p>
                    </td>
                    <td>
                        <p>{{ bond.count }}</p>
                    </td>
                    <td>
                        <p>{{ (bond.market_price * bond.count).toFixed(0) }}</p>
                    </td>
                    <td>
                        <p>{{ (bond.market_price / bond.nominal * 100).toFixed(1) + '%' }}</p>
                    </td>
                    <td>
                        <p>{{ (bond.coupon_profitability * 100).toFixed(1) + '%' }}</p>
                    </td>
                    <td>
                        <p>{{ (bond.profitability * 100).toFixed(1) + '%' }}</p>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

</template>

<style>
td {
    @apply p-2 border border-neutral-300
}

.active-sort {
    @apply bg-neutral-200 border-2
}
th {
    @apply hover:bg-neutral-200
}
</style>