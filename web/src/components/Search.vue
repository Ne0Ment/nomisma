<script setup>
import { ref, toRef, computed } from 'vue'
import { sort } from 'fast-sort';
import SearchSettings from './searchcomponents/SearchSettings.vue';
import SearchList from './searchcomponents/SearchList.vue';
import SearchBar from './searchcomponents/SearchBar.vue';

const props = defineProps({
    bonds: Array
});

const allBonds = toRef(props, 'bonds');
const settings = ref(null);
const searchBar = ref('');
const searchResults = ref([]);

function Refilter() {
    let results = allBonds.value.filter(bond =>
        (settings.value.sectors.includes(bond.sector)) &&
        (bond.maturity_date < settings.value.maturityEndDate) &&
        (bond.maturity_date > settings.value.maturityStartDate) &&
        (bond.coupons.every(t => settings.value.couponMonths.includes(t.coupon_date.getMonth()))))
    if (settings.value.sorting == 0) {
        if (settings.value.sortingDirection) {
            results = sort(results).desc(t => t.profitability)
        } else {
            results = sort(results).asc(t => t.profitability)
        }
    }
    searchResults.value = results;
}

function UpdateSettings(s) {
    settings.value = s;
    Refilter();
}

function UpdateSearchbar(val) {
    searchBar.value = val;
    Refilter();
}
</script>

<template>
    <div class="flex flex-row h-full mt-2 overflow-hidden gap-2">
        <div class="flex flex-col grow">
            <SearchBar @update-search="UpdateSearchbar" />
            <SearchList :all-bonds="allBonds" :bonds="searchResults"/>
        </div>
        <div class="flex flex-col">
            <SearchSettings @update-settings="UpdateSettings" />
        </div>
    </div>
</template>