<script setup>

const props = defineProps({
    bonds: Array
});

</script>

<template>
    <table class="flex flex-col overflow-auto">
        <div v-for="bond of bonds" key="bond.figi" class="border-2 border-neutral-400 my-2 rounded-md shadow-xl mr-4">
            <div class="hover:bg-neutral-200">
                <div class="flex flex-row p-2 gap-2">
                    <div class="flex flex-col grow">
                        <p>наименование: {{ bond.name }}</p>
                        <p>тикер: {{ bond.ticker }}</p>
                    </div>
                    <div class="flex flex-col">
                        <p> {{ (bond.profitability*100).toFixed(2)+'%' }} </p>
                    </div>
                </div>

            </div>
        </div>
    </table>
</template>