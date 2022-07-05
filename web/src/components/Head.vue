<script setup>
import { ref, onMounted, computed } from 'vue';
import Cookies from 'js-cookie'
import PortfolioDisplayVue from './PortfolioDisplay.vue';

const props = defineProps({
    tabs: Array,
    chosenTab: Number,
    sums: Object
});

const emit = defineEmits(['ChangeTab']);

const displayDropDown = ref(false);
const displayPortfolio = ref(true)
const chosenOption = ref(0);

const options = computed(() => {
    return [{ id: 0, value: props.sums.nominalValue, text: 'номинальная стоимость: ' },
            { id: 1, value: props.sums.marketValue, text: 'рыночная стоимость: ' }]
});

if (Cookies.get('head-portfolio')) {
    chosenOption.value = Cookies.get('head-portfolio');
}

function ChangeTab(tabId) {
    emit('ChangeTab', tabId);
}

function ChangePortfolioDisplay(newId) {
    chosenOption.value = newId;
    displayDropDown.value = false;
    Cookies.set('head-portfolio', newId);
    setTimeout(() => {
        displayPortfolio.value = true;
    }, 300)
}

</script>

<template>
    <div class="flex flex-row border-b-4">
        <h1 class="text-3xl font-bold mr-5 m-auto">облиги</h1>
        <div class="flex flex-col m-auto border-2 border-neutral-500 rounded-lg">
            <button class="self-start py-1 px-3" @click="() => { displayDropDown = true; displayPortfolio = false }">
                {{ options[chosenOption].value + ' руб' }}
            </button>
            <div class="optionsDiv overflow-clip"
                :class="{ 'max-h-20 max-w-lg': displayDropDown, 'max-h-0 max-w-0': !displayDropDown }">
                <div class="flex flex-col max-h-full truncate">
                    <button class=" hover:bg-neutral-200 rounded-lg p-1" v-for="option of options"
                        @click="() => ChangePortfolioDisplay(option.id)">
                        {{ option.text + ' ' + option.value + ' руб' }}
                    </button>
                </div>
            </div>
        </div>
        <div class="flex flex-row-reverse gap-2 grow">
            <div v-for="tab of tabs" class="pb-2">
                <button @click="ChangeTab(tab.id)" :class="tab.id == chosenTab ? 'activebutton' : 'passivebutton'"
                    :disabled="tab.id == chosenTab">
                    {{ tab.name }}
                </button>
            </div>
        </div>
    </div>
</template>


<style>
.optionsDiv {
    transition: max-width 0.3s, max-height 0.3s;
}
</style>
