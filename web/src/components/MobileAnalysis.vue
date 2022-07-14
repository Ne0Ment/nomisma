<script setup>

import { ref, toRef, computed, onMounted, watch } from 'vue'
import { sort } from 'fast-sort';
import MobilePortfolios from './MobilePortfolios.vue';
import MobileAnalysisSettings from './MobileAnalysisSettings.vue';
import MobileGraphDisplay from './MobileGraphDisplay.vue';

const props = defineProps({
    portfolios: {
        type: Array,
        default: []
    }
});
const portfolios = toRef(props, 'portfolios');
const chosenBonds = ref([]);
const calcSettings = ref();

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

function SetNewBonds(newBonds) {
    chosenBonds.value = newBonds;
}

function SetNewSettings(newSettings) {
    calcSettings.value = newSettings;
}

</script>

<template>
    <div class="flex flex-col overflow-hidden">
        <div class="flex flex-row">
            <MobilePortfolios @update-bonds="SetNewBonds" v-if="portfolios.length!=0" :portfolios="portfolios" />
            <MobileAnalysisSettings v-if="portfolios.length!=0" @update-settings="SetNewSettings"/>
        </div>
        <MobileGraphDisplay :display-data="displayData"/>
    </div>
</template>