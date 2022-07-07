<script setup>
import { ref, computed } from 'vue';
import { copyText } from 'vue3-clipboard'
import { useIntersectionObserver } from '@vueuse/core'
const props = defineProps({
    bond: Object
});
const shouldRender = ref(false);
const targetEl = ref(null);
const displayOptions = ref(false);

const sectormap = {
    'government': 'государственный',
    'municipal': 'муниципальный',
    'financial': 'финансовый',
    'industrials': 'индустриальный',
    'consumer': 'потребительский',
    'real_estate': 'недвижимость',
    'energy': 'энергетика',
    'telecom': 'телеком',
    'materials': 'материалы',
    'utilities': 'utilities',
    'health_care': 'здравоохранение',
    'it': 'ит',
    'other': 'другие'
}

const { stop } = useIntersectionObserver(
    targetEl,
    ([{ isIntersecting }]) => {
        if (isIntersecting) {
            shouldRender.value = true;
            stop();
        }
    });
</script>

<template>
    <div ref="targetEl" class="p-2 hover:bg-neutral-200 border-2 border-neutral-400 rounded-md mr-4 text-base"
        @click="{ displayOptions = !displayOptions; }">
        <div v-if="shouldRender" class="flex flex-row">
            <div class="flex flex-col overflow-hidden">
                <p>{{ bond.name }}</p>
                <p class="mt-auto select-text hover:italic hover:font-bold" @click.stop="copyText(bond.ticker)">{{
                        bond.ticker
                }}</p>
                <div class="options-div flex flex-col w-full overflow-hidden"
                    :class="displayOptions ? 'max-h-80' : 'max-h-0'">
                    <p v-if="bond.coupons.length">купоны</p>
                    <div class="overflow-auto w-full pr-3">
                        <table class="overflow-auto table-auto border-collapse w-full" v-if="bond.coupons.length">
                            <tr class="w-full">
                                <td class="p-1"> дата </td>
                                <td class="p-1"> сумма </td>
                                <td class="p-1"> номер </td>
                            </tr>
                            <tr v-for="coupon of bond.coupons.slice().reverse()" :key="coupon.coupon_number"
                                class="border-2 border-black">
                                <td> {{ [coupon.coupon_date.getUTCDate(), coupon.coupon_date.getUTCMonth() + 1,
                                    coupon.coupon_date.getUTCFullYear()].join('.')
                                }} </td>
                                <td> {{ coupon.pay_one_bond }} </td>
                                <td> {{ coupon.coupon_number }} </td>
                            </tr>
                        </table>
                    </div>
                </div>
            </div>
            <div class="flex flex-col border-l-2 border-neutral-500 pl-2 ml-auto overflow-hidden">
                <div class="flex flex-row gap-4">
                    <p>текущая доходность</p>
                    <p class="ml-auto">{{ (bond.coupon_profitability * 100).toFixed(1) + '%' }}</p>
                </div>
                <div class="flex flex-row gap-4">
                    <p>доходность к погашению</p>
                    <p class="ml-auto">{{ (bond.profitability * 100).toFixed(1) + '%' }}</p>
                </div>
                <div class="flex flex-row gap-4">
                    <p>дата погашения</p>
                    <p class="ml-auto">{{ [bond.maturity_date.getUTCDate(), bond.maturity_date.getUTCMonth() + 1,
                        bond.maturity_date.getUTCFullYear()].join('.')
                    }}</p>
                </div>
                <div class="options-div" :class="displayOptions ? 'max-h-60' : 'max-h-0'">
                    <div class="flex flex-row gap-4">
                        <p>номинал</p>
                        <p class="ml-auto">{{ bond.nominal }}</p>
                    </div>
                    <div class="flex flex-row gap-4">
                        <p>рыночная стоимость</p>
                        <p class="ml-auto">{{ bond.market_price.toFixed(2) }}</p>
                    </div>
                    <div class="flex flex-row gap-4">
                        <p>сектор</p>
                        <p class="ml-auto">{{ sectormap[bond.sector] }}</p>
                    </div>
                    <div class="flex flex-row gap-4">
                        <p>амортизация</p>
                        <p class="ml-auto">{{ bond.amortization_flag ? 'да' : 'нет' }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<style>
.options-div {
    transition: max-height 0.2s ease-in-out;
}
</style>