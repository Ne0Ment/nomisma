<script setup>
import { ref, toRef } from 'vue';

const emit = defineEmits(['add-portfolio']);

const props = defineProps({
    portfolios: {
        type: Array,
        default: []
    }
});

const portfolios = toRef(props, 'portfolios');
const showOptions = ref(false);

function AddPortfolio(portfolio){
    emit('add-portfolio', portfolio.bonds.map(bond => bond.figi));
}
</script>

<template>
    <div class="flex flex-col border-neutral-200 border-2 min-w-max">
        <button @click="() => {showOptions = !showOptions}" class="hover:bg-neutral-200">
            <p class="m-1 text-base"> добавить из портфеля </p>
        </button>
        <div class="grid grid-cols-2 gap-2 sd overflow-clip px-1" :class="showOptions ? 'max-h-20' : 'max-h-0'">
            <button class="px-2 self-center text-center border-2 border-neutral-200 hover:bg-neutral-200" 
                    v-for="portfolio in portfolios"
                    @click="AddPortfolio(portfolio)">
                <p class="text-center self-center">{{ portfolio.name }}</p>
            </button>
        </div>
    </div>
</template>

<style>
.sd {
    transition: max-height 0.1s ease-in-out;
}
</style>