<script setup>
import { ref, onMounted, toRef, computed, watch } from 'vue';
import chroma from "chroma-js";
import { Pie } from 'vue-chartjs';
import { Chart, ArcElement, Legend } from 'chart.js'
Chart.register(ArcElement, Legend);

const emit = defineEmits(['SelectGroup'])

const props = defineProps({
    groups: Array,
    chosenGroup: Number
})

const groups = toRef(props, 'groups');
const chartElem = ref(null);

const chartScale = chroma.scale(['#b8e9d4', '#f4985a', '#12243f']).mode('lch')

const chartData = computed(() => {
    return {
        labels: groups.value ? groups.value.map(t => t.key) : [0],
        datasets: [{
            data: groups.value ? groups.value.map(t => t.sum) : [0]
        }],
    }
});

const chartOptions = computed(() => {
    return {
        responsive: true,
        spacing: 2,
        animation: {
            duration: 400
        },
        hoverBorderColor: '#000000',
        backgroundColor: groups.value ? chartScale.colors(groups.value.length) : 0,
        plugins: {
            legend: {
                position: 'left',
                align: 'center',
                display: true
            }
        },
        maintainAspectRatio: true,
        aspectRatio: 1.5,
        onClick: (e) => {
            let found = chartElem.value.chart.getElementsAtEventForMode(e, 'nearest', { intersect: true }, true)[0];
            if (found) {
                emit('SelectGroup', found.index)
            }
        }
    }
});

</script>

<template>
    <div class="m-auto w-1/2 flex flex-col content-start">
        <Pie :chart-data="chartData" :chart-options="chartOptions" ref="chartElem" class="mt-0 pt-0" />
    </div>
</template>