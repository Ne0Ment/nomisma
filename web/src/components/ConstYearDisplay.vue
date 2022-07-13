<script setup>
import { useIntersectionObserver } from '@vueuse/core'
import { ref, onMounted } from 'vue';
import BarChart from './BarChart.vue';

const props = defineProps({
    year: String,
    data: Object,
});

const emit = defineEmits(['set-count']);

const shouldRender = ref(false);
const targetEl = ref(null);
const chosenMonth = ref(-1);
const displayDropDown = ref(false);

const { stop } = useIntersectionObserver(
    targetEl,
    ([{ isIntersecting }]) => {
        if (isIntersecting) {
            shouldRender.value = true;
            stop();
        }
    });

function UpdateChosen(month) {
    if ((chosenMonth.value == month) && (displayDropDown.value)) {
        displayDropDown.value = false;
    } else {
        chosenMonth.value = month;
        displayDropDown.value = true;
    }
};

function HideDropDown() {
    UpdateChosen(chosenMonth.value)
}

function SetCount(index, count) {
    emit('set-count', {bond: index, count: count});
}
</script>

<template>
    <div class="flex flex-col w-full">
        <div ref="targetEl" class="flex flex-row w-full">
            <BarChart v-if="shouldRender" class="w-full min-w-0 grow" :displayData="data.monthSum"
                :chosen-bar="chosenMonth" :highlight-month="displayDropDown" @display-month="UpdateChosen" />
            <div class="flex flex-col px-3 py-2 whitespace-nowrap border-2">
                <p class="content-center">{{ year }}</p>
                <p>среднее: {{ (data.monthSum.reduce((a, b) => a + b, 0) / data.monthSum.length).toFixed(0) }}</p>
                <p>сумма: {{ data.monthSum.reduce((a, b) => a + b, 0).toFixed(0) }}</p>
            </div>
        </div>
        <div class="border-b-neutral-200 collapsableDiv p-2 m-2 flex flex-row overflow-clip"
            :class="{ 'max-h-80': displayDropDown, 'max-h-0': !displayDropDown }">
            <div class="flex flex-row w-full">
                <div class="table-wrp block max-h-full overflow-auto text-sm w-full">
                    <table class="w-full overflow-auto">
                        <thead class="text-sm">
                            <td>кол-во</td>
                            <td>дата</td>
                            <td>тикер</td>
                            <td>наименование</td>
                            <td>сумма</td>
                            <td>к погаш.</td>
                            <td>тек.</td>
                            <td>действия</td>
                        </thead>
                        <tbody>
                            <tr v-if="chosenMonth != -1" class="py-2 border-2 border-neutral-300 text-sm hover:bg-neutral-200"
                                v-for="(bond, index) of data.monthCoupons[chosenMonth]"
                                :class="bond.display ? '' : 'hidden'">
                                <td>{{ bond.count }}</td>
                                <td class="px-2 py-1">{{ [bond.date.getUTCDate(), bond.date.getUTCMonth() + 1,
                                    bond.date.getUTCFullYear()].join('.')
                                }}</td>
                                <td class="px-2 py-1">{{ bond.ticker }}</td>
                                <td class="px-2 py-1">{{ bond.name }}</td>
                                <td class="px-2 py-1">{{ (bond.one_pay ? bond.one_pay.toFixed(0) : '?') }}</td>
                                <td class="px-2 py-1">{{ (bond.profitability * 100).toFixed(2) + '%' }}</td>
                                <td class="px-2 py-1">{{ (bond.coupon_profitability * 100).toFixed(2) + '%' }}</td>
                                <td class="flex flex-row px-2 py-1">
                                    <button class="grow" @click="SetCount(bond.ticker, bond.count+1)">
                                        +
                                    </button>
                                    <button class="grow" @click="SetCount(bond.ticker, bond.count-1)">
                                        -
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <button class="text-4xl text-neutral-600 max-h-full overflow-hidden self-start" @click="HideDropDown()">
                    ×
                </button>
            </div>
        </div>
    </div>

</template>

<style>
.collapsableDiv {
    transition: max-height 0.3s;
}
</style>