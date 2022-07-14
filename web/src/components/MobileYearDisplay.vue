<script setup>
import { useIntersectionObserver } from '@vueuse/core'
import { ref, onMounted } from 'vue';
import MobileBarChart from './MobileBarChart.vue';

const props = defineProps({
    year: String,
    data: Object,
});

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

</script>

<template>
    <div class="flex flex-col mx-3">
        <div ref="targetEl" class="flex flex-col w-full z-10">
            <div class="flex flex-row text-sm gap-2">
                <p class="mr-auto">{{ year }}</p>
                <p>сумма: {{ (data.monthSum.reduce((a, b) => a + b, 0)).toFixed(0) }}</p>
                <p>среднее: {{ (data.monthSum.reduce((a, b) => a + b, 0) / data.monthSum.length).toFixed(0) }}</p>
            </div>
            <MobileBarChart v-if="shouldRender" class="grow min-w-0" :displayData="data.monthSum"
                :chosen-bar="chosenMonth" :highlight-month="displayDropDown" @display-month="UpdateChosen" />
            <!-- <div class="flex flex-col px-3 py-2 whitespace-nowrap border-2">
                <p class="content-center">{{ year }}</p>
                <p>среднее: {{ (data.monthSum.reduce((a, b) => a + b, 0) / data.monthSum.length).toFixed(0) }}</p>
                <p>сумма: {{ data.monthSum.reduce((a, b) => a + b, 0).toFixed(0) }}</p>
            </div> -->
        </div>
        <!-- <div class="border-b-neutral-200 collapsableDiv flex flex-row overflow-clip"
            :class="{ 'max-h-80': displayDropDown, 'max-h-0': !displayDropDown }">
            <div class="flex flex-row">
                <table class="table-fixed border-collapse overflow-auto max-h-full block text-xs pr-2 grow">
                    <tr class="text-center text-xs">
                        <td>дата</td>
                        <td>тикер</td>
                        <td>наименование</td>
                        <td>доходность к погашению</td>
                        <td>купонная доходность</td>
                        <td>текущая стоимость</td>
                        <td>сумма, руб</td>
                        <td>портфель</td>
                        <td>операция</td>
                    </tr>
                    <tr v-if="chosenMonth != -1" class="py-2 border-2 border-neutral-300"
                        v-for="bond of data.monthCoupons[chosenMonth]">
                        <td class="px-2 py-1">{{ [bond.date.getUTCDate(), bond.date.getUTCMonth() + 1,
                            bond.date.getUTCFullYear()].join('.')
                        }}</td>
                        <td class="">{{ bond.ticker }}</td>
                        <td class="">{{ bond.name }}</td>
                        <td class="">{{ (bond.profitability * 100).toFixed(2) + '%' }}</td>
                        <td class="">{{ (bond.coupon_profitability * 100).toFixed(2) + '%' }}</td>
                        <td class="">{{ bond.market_sum ? bond.market_sum.toFixed(0) : '-' }}</td>
                        <td class="">{{ (bond.all_pay ? bond.all_pay.toFixed(0) : '?') }}</td>
                        <td class="">{{ bond.portfolioName }}</td>
                        <td class="">{{ bond.type }}</td>
                    </tr>
                </table>
                <button class="text-4xl text-neutral-600 max-h-full overflow-hidden self-start pr-5"
                    @click="HideDropDown()">
                    ×
                </button>
            </div>
        </div> -->
    </div>

</template>

<style>
.collapsableDiv {
    transition: max-height 0.3s ease-in-out;
}
</style>