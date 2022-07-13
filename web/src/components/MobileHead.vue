<script setup>
import { ref, onMounted, computed } from 'vue';
import Cookies from 'js-cookie'

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
    <div class="flex flex-row border-b-4 gap-1">
        <p class="text-2xl font-bold m-auto">облиги</p>
        <!-- <div class="flex flex-col m-auto border-2 text-sm self-center my-auto">
            <button class="self-start py-1 px-3 hover:bg-neutral-200"
                @click="() => { displayDropDown = true; displayPortfolio = false }">
                {{ options[chosenOption].value + ' р' }}
            </button>
            <div class="absolute optionsDiv overflow-clip z-10 bg-white shadow-xl self-center"
                :class="{ 'max-h-20 max-w-lg': displayDropDown, 'max-h-0 max-w-0': !displayDropDown }">
                <div class="flex flex-col max-h-full truncate">
                    <button class=" hover:bg-neutral-200 p-1" v-for="option of options"
                        @click="() => ChangePortfolioDisplay(option.id)">
                        {{ option.text + ' ' + option.value + ' р' }}
                    </button>
                </div>
            </div>
        </div> -->
        <div class="flex flex-row-reverse m-auto border-2 text-sm self-center my-auto">
            <div v-for="tab of tabs">
                <button @click="ChangeTab(tab.id)" :class="tab.id == chosenTab ? 'activebutton-m' : 'passivebutton-m'"
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
.passivebutton-m {
  @apply text-base p-2 hover:bg-neutral-600 hover:text-white
}

.activebutton-m {
  @apply text-base p-2 bg-neutral-600 text-white
}
</style>