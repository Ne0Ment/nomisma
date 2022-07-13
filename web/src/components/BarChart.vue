<script setup>
import { reactive, computed, ref } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { refAutoReset } from '@vueuse/core';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const emit = defineEmits(['DisplayMonth']);

const props = defineProps({
  displayData: {
    type: Array,
    default: []
  },
  chosenBar: {
    type: Number,
    default: -1
  },
  highlightMonth: {
    type: Boolean,
    default: true
  }
});


const chartElem = ref(null);
const containerElem = ref(null);

function ClearChoice() {
  barSettings.barColors = Array(12).fill(barSettings.baseColor);
  barSettings.barBorders = Array(12).fill(barSettings.baseBorder);
}

function ScrollEmit(monthClicked) {
  emit('DisplayMonth', monthClicked);
  containerElem.value.scrollIntoView({ behavior: 'smooth' });
}

const chartOptions = computed(() => {
  let weights = Array(12).fill("normal");
  if ((props.highlightMonth) && (props.chosenBar != -1)) {
    weights[props.chosenBar] = "bold";
  }
  return {
    responsive: true,
    maintainAspectRatio: true,
    aspectRatio: 3,
    animation: false,
    plugins: {
      legend: {
        display: false
      }
    },
    scales: {
      x: {
        ticks: {
          font: {
            weight: weights
          }
        }
      }
    },
    onClick: (e) => {
      let found = chartElem.value.chart.getElementsAtEventForMode(e, 'nearest', { intersect: true }, true)[0];
      if (found) {
        let monthClicked = found.index;
        ScrollEmit(monthClicked);
      }
    }
  }
});

const chartData = computed(() => {
  let borders = Array(12).fill("#FFFFFF");
  if ((props.highlightMonth) && (props.chosenBar != -1)) {
    borders[props.chosenBar] = "#525252";
  }
  return {
    labels: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
    datasets: [{
      data: props.displayData,
      backgroundColor: '#e5e5e5',
      borderColor: borders,
      borderWidth: 2
    }]
  }
});

const monthButtons = ref([
  { id: 0, name: 'Январь' },
  { id: 1, name: 'Февраль' },
  { id: 2, name: 'Март' },
  { id: 3, name: 'Апрель' },
  { id: 4, name: 'Май' },
  { id: 5, name: 'Июнь' },
  { id: 6, name: 'Июль' },
  { id: 7, name: 'Август' },
  { id: 8, name: 'Сентябрь' },
  { id: 9, name: 'Октябрь' },
  { id: 10, name: 'Ноябрь' },
  { id: 11, name: 'Декабрь' }
]);

</script>

<template>
  <div ref="containerElem" class="flex flex-col overflow-auto">
    <Bar :chart-options="chartOptions" :chart-data="chartData" ref="chartElem" />
    <div class="flex flex-row w-full">
      <div class="invisible">
        <p>{{ "....." }}</p>
      </div>
      <div v-for="b of monthButtons" class="grow z-10 -translate-y-5" @click="ScrollEmit(b.id)">
        <button class="text-sm"></button>
      </div>
    </div>

  </div>
</template>

<style>
canvas {
  width: 100% !important;
}
</style>