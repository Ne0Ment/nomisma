<script setup>
import { onMounted, ref } from 'vue';

const emit = defineEmits(['NewOptions'])

const pieOptions = ref([
    { id: 0, active: true, name: 'сектор'},
    { id: 1, active: false, name: 'год погашения'},
    { id: 2, active: false, name: 'кол-во купонов'},
    { id: 3, active: false, name: 'аморатизация'},
    { id: 4, active: false, name: 'плавающий купон'},
]);

function SelectOption(id) {
    pieOptions.value = pieOptions.value.map(t => {
        const newT = {...t};
        newT.active = (t.id==id)
        return newT;
    });
};

function EmitOptions() {
    emit('NewOptions', pieOptions.value.filter(t => t.active)[0].id);
}

onMounted(() => {
    EmitOptions();
});

</script>

<template>
<div class="flex flex-col gap-2 ml-auto">
    <p class="text-lg">диаграмма</p>
    <button v-for="option in pieOptions" :key="option.id"
        class="p-1 border-2 border-black hover:bg-neutral-600 hover:text-white" @click="{SelectOption(option.id); EmitOptions()}"
        :class="option.active ? 'bg-neutral-600 text-white' : 'bg-white text-black'">
        {{ option.name }}
    </button>
</div>
</template>