<script setup>
import { ref, toRef, computed, onMounted, watch } from 'vue'
import { sort } from 'fast-sort';

import TableFilters from './TableFilters.vue';
import ConstructorPortfolios from './ConstructorPortfolios.vue';
import ConstGraphs from './ConstGraphs.vue';

const props = defineProps({
    portfolios: Array,
    allBonds: Array
});

const portfolios = toRef(props, 'portfolios');
const allBonds = ref(props.allBonds.map(b => {
    let bond = { ...b };
    bond.count = 0;
    return bond;
}));
const actions = ref();
const filters = ref([]);

const tickerMap = computed(() => {
    let t = {};
    for (let i = 0; i < allBonds.value.length; i++) {
        t[allBonds.value[i].ticker] = i;
    }
    return t;
})

function FilterBonds() {
    allBonds.value = allBonds.value.map(b => {
        let bond = { ...b };
        let ok = true;
        if (filters.value) {
            for (const filter of Object.keys(filters.value)) {
                if (!filters.value[filter][bond[filter]]) {
                    ok = false;
                    break;
                }
            }
        }
        if (ok || (bond.count!=0)) {
            bond.display = true;
        } else {
            bond.display = false;
        }
        return bond;
    });
}

function CalcActions(bond = undefined) {
    let data = {};
    let couponDate, year, month, couponVal;
    let taxCheckDate = new Date(); taxCheckDate.setFullYear(taxCheckDate.getFullYear() + 3);
    if (bond) {
    } else {
        for (const bond of allBonds.value) {
            if (bond.coupons) {
                for (let coupon of bond.coupons) {
                    couponDate = coupon.coupon_date
                    year = couponDate.getUTCFullYear();
                    month = couponDate.getUTCMonth();
                    if (data[year] == undefined) {
                        data[year] = {};
                        data[year].monthSum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
                        data[year].monthCoupons = Array.from(Array(12), () => []);
                    }
                    couponVal = coupon.pay_one_bond * bond.count;
                    data[year].monthSum[month] += couponVal;
                    coupon.ticker = bond.ticker;
                    coupon.name = bond.name;
                    coupon.all_pay = couponVal;
                    data[year].monthCoupons[month].push({
                        ticker: bond.ticker,
                        name: bond.name,
                        all_pay: couponVal,
                        one_pay: coupon.pay_one_bond,
                        type: 'купон',
                        date: couponDate,
                        display: bond.display,
                        portfolioName: bond.portfolioName,
                        profitability: bond.profitability,
                        coupon_profitability: bond.coupon_profitability,
                        count: bond.count
                    });
                }
            }

        }
        for (const year of Object.keys(data)) {
            for (let month = 0; month < 12; month++) {
                data[year].monthCoupons[month] = sort(data[year].monthCoupons[month]).desc([
                    bond => bond.count,
                    bond => bond.date.getTime()
                ])
            }
        }
        if (Object.keys(data).length != 0) {
            actions.value = data;
        } else {
            let currentYear = (new Date()).getUTCFullYear();
            data = {};
            data[currentYear] = {};
            data[currentYear].monthSum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
            actions.value = data;
        }
    }
}

function AddPortfolioBonds(figis) {
    console.log(figis);
    allBonds.value = allBonds.value.map(b => {
        let bond = { ...b };
        if (figis.includes(bond.figi)) {
            bond.count += 1;
        }
        return bond;
    });
    CalcActions();
}

const tab = ref(0);

function UpdateFilters(v) {
    filters.value = v;
    FilterBonds();
    CalcActions();
}

function SetCount(d) {
    const index = tickerMap.value[d.bond];
    allBonds.value[index].count = d.count;
    CalcActions();
}

</script>

<template>
    <div class="flex flex-col overflow-hidden w-full">
        <div class="flex flex-row gap-2 mt-2">
            <button class="hover:bg-neutral-600 hover:text-white rounded-md p-1"
                :class="tab == 0 ? 'active-tab' : 'passive-tab'" @click="tab = 0">
                календарь
            </button>
            <!-- <button class="hover:bg-neutral-600 hover:text-white rounded-md p-1"
                :class="tab == 1 ? 'active-tab' : 'passive-tab'" @click="tab = 1">
                анализ
            </button>
            <button class="hover:bg-neutral-600 hover:text-white rounded-md p-1"
                :class="tab == 2 ? 'active-tab' : 'passive-tab'" @click="tab = 2">
                список
            </button> -->
        </div>
        <div class="flex flex-row h-full mt-2 overflow-hidden gap-2 w-full">
            <ConstGraphs v-if="(tab == 0)" :display-data="actions" @set-count="SetCount" />
            <div class="flex flex-col gap-4">
                <ConstructorPortfolios v-if="portfolios != []" :portfolios="portfolios" @add-portfolio="AddPortfolioBonds"/>
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