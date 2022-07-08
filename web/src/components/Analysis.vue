<script setup>
import { ref, toRef, computed, onMounted, watch } from 'vue'
import { sort } from 'fast-sort';

import PortfolioDisplay from "./PortfolioDisplay.vue";
import CalcSettings from './CalcSettings.vue';
import DataDisplay from './DataDisplay.vue';
import PieAnalysis from './PieAnalysis.vue';
import PieSettings from './PieSettings.vue';

const props = defineProps({
    portfolios: Array
});

const portfolios = toRef(props, 'portfolios');
const chosenBonds = ref([]);
const calcSettings = ref();
const pieMode = ref();
const selectedGroup = ref(0);

const displayData = computed(() => {
    if (calcSettings.value) {
        let data = {};
        let couponDate, year, month, couponVal, nominalVal, repayDate;
        let taxCheckDate = new Date(); taxCheckDate.setFullYear(taxCheckDate.getFullYear() + 3);
        for (const bond of chosenBonds.value) {
            if (calcSettings.value.coupons) {
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
                    if (calcSettings.value.tax) {
                        couponVal *= 0.87;
                    }
                    data[year].monthSum[month] += couponVal;
                    coupon.ticker = bond.ticker;
                    coupon.name = bond.name;
                    coupon.all_pay = couponVal;
                    data[year].monthCoupons[month].push({
                        ticker: bond.ticker,
                        name: bond.name,
                        all_pay: couponVal,
                        type: 'купон',
                        date: couponDate,
                        portfolioName: bond.portfolioName,
                        profitability: bond.profitability,
                        coupon_profitability: bond.coupon_profitability
                    });
                }
            }
        }

        if (calcSettings.value.repayments) {
            for (const bond of chosenBonds.value) {
                repayDate = bond.maturity_date;
                year = repayDate.getUTCFullYear();
                if (year < 2000) {
                    continue;
                }
                month = repayDate.getUTCMonth();
                if (data[year] == undefined) {
                    data[year] = {};
                    data[year].monthSum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
                    data[year].monthCoupons = Array.from(Array(12), () => []);
                }
                nominalVal = bond.nominal * bond.count;
                if ((calcSettings.value.tax === true) && (couponDate > taxCheckDate)) {
                    nominalVal *= 0.87;
                }
                data[year].monthCoupons[month].push({
                    ticker: bond.ticker,
                    name: bond.name,
                    all_pay: nominalVal,
                    type: 'погашение',
                    date: repayDate,
                    portfolioName: bond.portfolioName,
                    profitability: bond.profitability,
                    coupon_profitability: bond.coupon_profitability,
                    market_sum: bond.market_price * bond.count
                });
                data[year].monthSum[month] += nominalVal;
            }
        }

        for (const year of Object.keys(data)) {
            for (let month = 0; month < 12; month++) {
                data[year].monthCoupons[month].sort((a, b) => {
                    return a.date.getTime() > b.date.getTime() ? 1 : -1;
                });
            }
        }

        if (Object.keys(data).length != 0) {
            return data;
        } else {
            let currentYear = (new Date()).getUTCFullYear();
            data = {}
            data[currentYear] = {}
            data[currentYear].monthSum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
            return data
        }
    } else {
        return [];
    }

});

const pieGroups = computed(() => {
    const pieKeys = {
        0: 'sector',
        1: 'maturtyYear',
        2: 'amortization_flag',
        3: 'floating_coupon_flag'
    }
    const vals = groupBy(chosenBonds.value, pieKeys[pieMode.value]);
    let groups = [];
    for (const [key, val] of Object.entries(vals)) {
        groups.push({
            key: key,
            bonds: val,
            sum: val.map(t => t.market_price * t.count).reduce((a, b) => a + b, 0)
        });
    }
    return sort(groups).desc(t => t.sum);

});

const groupBy = function (xs, key) {
    return xs.reduce(function (rv, x) {
        (rv[x[key]] = rv[x[key]] || []).push(x);
        return rv;
    }, {});
};

function SetNewBonds(newBonds) {
    chosenBonds.value = newBonds;
    selectedGroup.value = 0;
}

function SetNewSettings(newSettings) {
    calcSettings.value = newSettings;
}

function SetNewPieSettings(newSettings) {
    pieMode.value = newSettings;
}

function SelectGroup(t) {
    selectedGroup.value = t;
}
const tab = ref(1);

</script>

<template>
    <div class="flex flex-col">
        <div class="flex flex-row gap-2 mt-2">
            <button class="hover:bg-neutral-600 hover:text-white rounded-md p-1"
                :class="tab == 0 ? 'active-tab' : 'passive-tab'" @click="tab = 0">
                календарь
            </button>
            <button class="hover:bg-neutral-600 hover:text-white rounded-md p-1"
                :class="tab == 1 ? 'active-tab' : 'passive-tab'" @click="tab = 1">
                анализ
            </button>
        </div>
        <div class="flex flex-row h-full mt-2 overflow-hidden gap-2">
            <DataDisplay v-if="(tab == 0)" :display-data="displayData" />
            <PieAnalysis v-if="(tab == 1)" :groups="pieGroups" :chosen-group="selectedGroup" @select-group="" />
            <div class="flex flex-col gap-4">
                <PortfolioDisplay @update-bonds="SetNewBonds" v-if="portfolios != []" :portfolios="portfolios" />
                <CalcSettings v-if="(tab == 0)" @update-settings="SetNewSettings" />
                <PieSettings v-if="(tab == 1)" @new-options="SetNewPieSettings" />
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