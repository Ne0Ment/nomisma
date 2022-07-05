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

const chartOptions = reactive({
  responsive: true,
  maintainAspectRatio: true,
  aspectRatio: 3,
  animation: false,
  plugins: {
    legend: {
      display: false
    }
  },
  onClick: (e) => {
    let found = chartElem.value.chart.getElementsAtEventForMode(e, 'nearest', { intersect: true }, true)[0];
    if (found) {
      let monthClicked = found.index;
      emit('DisplayMonth', monthClicked);
      containerElem.value.scrollIntoView({ behavior: 'smooth' });
    }
  }
});

const chartData = computed(() => {
  let borders = Array(12).fill("#FFFFFF");
  if ((props.highlightMonth) && (props.chosenBar!=-1)) {
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
</script>

<template>
  <div ref="containerElem">
    <Bar :chart-options="chartOptions" :chart-data="chartData" ref="chartElem" />
  </div>
</template>