<script setup>
import { computed, onMounted, watch, toRef, ref } from 'vue';

const props = defineProps({
    allBonds: Array
});

const emit = defineEmits(['EmitFilters']);

const allBonds = toRef(props, 'allBonds');

const allowList = [
    'sector',
    'amortization_flag',
    'floating_coupon_flag',
    'maturityYear',
    'coupon_quantity_per_year',

];

const sectorMap = {
    government: 'государственый',
    consumer: 'потребительский',
    financial: 'финансовый',
    real_estate: 'недвижимость',
    industrials: 'индустриальный',
    it: 'ит',
    telecom: 'телеком',
    materials: 'материалы',
    energy: 'энергетика',
    other: 'другое',
    health_care: 'здравоохранение',
    municipal: 'муниципальный',
    true: 'да',
    false: 'нет'
};

const allowNames = {
    sector: 'сектор',
    amortization_flag: 'амортизация',
    floating_coupon_flag: 'плавающий купон',
    maturityYear: 'год погашения',
    coupon_quantity_per_year: 'кол-во купонов',
};

const filters = ref({});

function CalcFilters() {
    let a = {};
    if (allBonds.value) {
        for (const bond of allBonds.value) {
            for (const key of Object.keys(bond)) {
                if (allowList.includes(key)) {
                    if (a[key] == undefined) {
                        a[key] = {};
                    }
                    if (a[key][bond[key]] == undefined) {
                        a[key][bond[key]] = true;
                    }
                }
            }
        }
    }
    filters.value = a;
}

watch(allBonds, (o, n) => {
    CalcFilters();
})

// const filters = computed(() => {
//     let a = {};
//     if (allBonds.value) {
//         for (const bond of allBonds.value) {
//             for (const key of Object.keys(bond)) {
//                 if (allowList.includes(key)) {
//                     if (a[key] == undefined) {
//                         a[key] = {};
//                     }
//                     if (a[key][bond[key]] == undefined) {
//                         a[key][bond[key]] = true;
//                     }
//                 }
//             }
//         }
//     }
//     return a;
// });

function EmitFilters() {
    emit('EmitFilters', filters.value);
}

onMounted(() => {
    EmitFilters();
});

function Clear(key) {
    for (const i of Object.keys(filters.value[key])) {
        filters.value[key][i] = false;
    }
    EmitFilters();
};

function All(key) {
    for (const i of Object.keys(filters.value[key])) {
        filters.value[key][i] = true;
    }
    EmitFilters();
};

</script>

<template>
    <div class="flex flex-col overflow-auto pr-3 min-w-max gap-3">
        <div v-for="(i, k) of filters" class="flex flex-col">
            <div class="flex flex-row-reverse gap-2">
                <button class="selector-button" @click="Clear(k)">
                    ничто
                </button>
                <button class="selector-button" @click="All(k)">
                    все
                </button>
                <p class="text-lg mr-auto"> {{ allowNames[k] }} </p>
            </div>
            <div class="flex flex-col pl-3 gap-1">
                <div v-for="(item, key, index) of i" class="bg-neutral-200 flex flex-row">
                    <input type="checkbox" class="h-4 w-4 align-middle m-1" v-model="i[key]" @change="EmitFilters()" />
                    {{ sectorMap[key] || key }}
                </div>
            </div>
        </div>
    </div>

</template>

<style>
.selector-button {
    @apply border-neutral-200 hover:bg-neutral-200 border-2 px-1 h-fit self-center whitespace-nowrap
}
</style>