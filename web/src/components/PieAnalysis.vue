<script setup>
import { ref, onMounted, toRef, computed, watch } from 'vue';
import chroma from "chroma-js";
import { Pie } from 'vue-chartjs';
import { Chart, ArcElement, Legend, Tooltip } from 'chart.js'
Chart.register(ArcElement, Legend, Tooltip);

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
        }]
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
            },
            tooltips: {
                mode: 'index'
            }
        },
        maintainAspectRatio: true,
        aspectRatio: 2.8,
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
    <div class="mx-auto w-full flex flex-col content-center mt-0 pt-0 max-h-full">
        <Pie :chart-data="chartData" :chart-options="chartOptions" ref="chartElem" class="mt-0 pt-0" />
    </div>
</template>