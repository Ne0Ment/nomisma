<script setup>
import { ref, reactive, onMounted } from 'vue'
import Head from './components/Head.vue';
import Account from './components/Account.vue';
import Analysis from './components/Analysis.vue';
import Cookies from 'js-cookie';
import Search from './components/Search.vue';

if (Cookies.get('temp-key') == undefined) {
  Cookies.set('temp-key', '');
}

const tabs = ref([
  { id: 0, name: 'аккаунт', active: true },
  { id: 1, name: 'портфель', active: false },
  { id: 2, name: 'конструктор', active: false },
  { id: 3, name: 'поиск', active: false }
]);

const sums = reactive({
  nominalValue: '0',
  marketValue: '0'
})

const portfolios = ref([]);
const chosenTab = ref(0);
const fetched = ref(false);
const fetchedBonds = ref(false);
const bonds = ref([]);
const serverUrl = "http://127.0.0.1:5000";

if (Cookies.get('main-tab')) {
  chosenTab.value = parseInt(Cookies.get('main-tab'));
}

function FetchSums() {
  let tempKey = Cookies.get('temp-key')
  let payload = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ temp_key: tempKey })
  }
  fetch(serverUrl + "/GetPortfolioSums", payload)
    .then(t => t.text())
    .then(t => JSON.parse(t))
    .then(t => {
      if (t.status) {
        sums.nominalValue = t.nominal_sum.toLocaleString('en-US');
        sums.marketValue = t.market_sum.toLocaleString('en-US');
      } else {
        sums.nominalValue = '0';
        sums.marketValue = '0';
      }

    });
}

function FetchPortfolios() {
  let tempKey = Cookies.get('temp-key')
  let payload = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ temp_key: tempKey })
  }
  fetch(serverUrl + "/GetPortfolios", payload)
    .then(t => t.text())
    .then(t => JSON.parse(t))
    .then(t => {
      if (t['status']) {
        portfolios.value = t['portfolios'].filter(t => t.bonds.length != 0);
        if (portfolios.value) {
          for (let i = 0; i < portfolios.value.length; i += 1) {
            portfolios.value[i].active = true;
            for (let j = 0; j < portfolios.value[i].bonds.length; j++) {
              portfolios.value[i].bonds[j].portfolioName = portfolios.value[i].name;
              portfolios.value[i].bonds[j].maturity_date = new Date(Date.parse(portfolios.value[i].bonds[j].maturity_date))
              for (let k = 0; k < portfolios.value[i].bonds[j].coupons.length; k++) {
                portfolios.value[i].bonds[j].coupons[k].coupon_date = new Date(Date.parse(portfolios.value[i].bonds[j].coupons[k].coupon_date))
              }
            }
          }
        } else {
          portfolios.value = [];
        }
        fetched.value = true;
      } else {
        portfolios.value = [];
        fetched.value = true;
      }
    });
}

function FetchBonds() {
  let payload = {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  }
  fetch(serverUrl+'/GetAllBonds')
    .then(t => t.text())
    .then(t => JSON.parse(t))
    .then(t => {
      if (t['status']) {
        bonds.value = t.bonds;
        fetchedBonds.value = true;
      }
    })
}

function UpdateTab(newTab) {
  chosenTab.value = newTab;
  Cookies.set('main-tab', newTab);
  tabs.value = tabs.value.map(x => {
    if (x.id == newTab) {
      x.active = true;
    } else {
      x.active = false;
    }
    return x;
  })
}

function ToggleLogin(newState) {
  fetchedBonds.value = false;
  fetched.value = false;
  FetchSums();
  FetchPortfolios();
  FetchBonds();
}

onMounted(() => {
  FetchSums();
  FetchPortfolios();
  FetchBonds();
});
</script>

<template>
  <div class="flex flex-col p-5 font-mono h-full max-w-screen-xl self-center m-auto">
    <KeepAlive>

      <Head :tabs="tabs" :chosenTab="chosenTab" :sums="sums" @ChangeTab="(t) => UpdateTab(t)" />
    </KeepAlive>
    <KeepAlive>
      <Account v-if="chosenTab === 0" @ToggleLogin="ToggleLogin" />
    </KeepAlive>
    <KeepAlive>
      <Analysis v-if="((chosenTab === 1) && (fetched))" :portfolios="portfolios" />
    </KeepAlive>
    <KeepAlive>
      <Search v-if="((chosenTab === 3) && (fetchedBonds))" />
    </KeepAlive>
  </div>
</template>

<style>
@tailwind base;
@tailwind components;
@tailwind utilities;

.passivebutton {
  @apply text-lg rounded-xl p-2 hover:bg-neutral-600 hover:text-white
}

.activebutton {
  @apply text-lg rounded-xl p-2 bg-neutral-600 text-white
}

.formbutton {
  @apply m-1 p-2 mt-4 bg-white rounded-xl hover:bg-neutral-600 hover:text-white
}

.inputfield {
  @apply m-1 text-xl p-2
}
</style>