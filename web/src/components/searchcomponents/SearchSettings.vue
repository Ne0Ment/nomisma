<script setup>
import { ref, reactive, onMounted } from 'vue';

import flatPickr from 'vue-flatpickr-component';
import 'flatpickr/dist/flatpickr.css';
import monthSelectPlugin from 'flatpickr/dist/plugins/monthSelect/index.js'
import 'flatpickr/dist/plugins/monthSelect/style.css'
import { Russian } from "flatpickr/dist/l10n/ru.js"

function AddYears(date, yearCount) {
    date.setFullYear(date.getFullYear() + yearCount)
    return date;
}

const emit = defineEmits(['UpdateSettings'])

const settings = ref({
    sorting: [
        { id: 0, chosen: true, name: 'доходность к погашению' },
        { id: 1, chosen: false, name: 'текущая доходность' }
    ],
    sortingDirection: true, // true - downwards, false - upwards
    maturityStartDate: AddYears(new Date(), 1),
    maturityEndDate: AddYears(new Date(), 4),
    couponMonths: [
        { 'name': 'янв', active: true, id: 0 },
        { 'name': 'фев', active: true, id: 1 },
        { 'name': 'март', active: true, id: 2 },
        { 'name': 'апр', active: true, id: 3 },
        { 'name': 'май', active: true, id: 4 },
        { 'name': 'июнь', active: true, id: 5 },
        { 'name': 'июль', active: true, id: 6 },
        { 'name': 'авг', active: true, id: 7 },
        { 'name': 'сен', active: true, id: 8 },
        { 'name': 'окт', active: true, id: 9 },
        { 'name': 'ноя', active: true, id: 10 },
        { 'name': 'дек', active: true, id: 11 }],
    couponSelectMode: [
        { id: 0, active: true, name: 'один' },
        { id: 1, active: false, name: 'все' }
    ],
    sectors: [
        { id: 0, active: true, name: 'государственный', tname: 'government' },
        { id: 1, active: true, name: 'муниципальный', tname: 'municipal' },
        { id: 2, active: true, name: 'финансовый', tname: 'financial' },
        { id: 3, active: true, name: 'индустриальный', tname: 'industrials' },
        { id: 4, active: true, name: 'потребительский', tname: 'consumer' },
        { id: 5, active: true, name: 'недвижимость', tname: 'real_estate' },
        { id: 6, active: true, name: 'энергетика', tname: 'energy' },
        { id: 7, active: true, name: 'телеком', tname: 'telecom' },
        { id: 8, active: true, name: 'материалы', tname: 'materials' },
        { id: 9, active: true, name: 'utilities', tname: 'utilities' },
        { id: 10, active: true, name: 'здравоохранение', tname: 'health_care' },
        { id: 11, active: true, name: 'ит', tname: 'it' },
        { id: 12, active: true, name: 'другие', tname: 'other' }]
});

const choosingFilter = ref(false);
const choosingMonthMode = ref(false);
const vueFlatpickrIsStupid = reactive({
    g1: null,
    g2: null
});

function EmitSettings() {
    const settingsObj = { ...settings.value };
    settingsObj.couponMonths = settingsObj.couponMonths.filter(t => t.active).map(t => t.id);
    settingsObj.sectors = settingsObj.sectors.filter(t => t.active).map(t => t.tname);
    settingsObj.sorting = settingsObj.sorting.filter(t => t.chosen)[0].id;
    settingsObj.couponSelectMode = settingsObj.couponSelectMode.filter(t => t.active)[0].id;
    emit('UpdateSettings', settingsObj);
}

onMounted(() => {
    EmitSettings();
});
</script>

<template>
    <div class="flex flex-col overflow-auto pr-2 min-w-max">
        <div class="option-div">
            <p class="option-title">сортировка</p>
            <div class="flex flex-row">
                <div v-if="choosingFilter"
                    class="absolute bg-white flex flex-col grow border-neutral-600 border-2 shadow-xl">
                    <button v-for="option of settings.sorting" class="sort-button" @click="() => {
                        choosingFilter = false;
                        settings.sorting = settings.sorting.map(t => {
                            let newT = { ...t };
                            newT.chosen = newT.id == option.id;
                            return newT;
                        });
                        EmitSettings();
                    }">
                        {{ option.name }}
                    </button>
                </div>
                <button v-else class="grow self-center sort-button border-neutral-600 border-2"
                    @click="choosingFilter = true">
                    {{ settings.sorting.filter(t => t.chosen)[0].name }}
                </button>
                <button class="text-4xl p-1 self-center content-center text-center"
                    @click="{ settings.sortingDirection = !settings.sortingDirection; EmitSettings(); }">
                    {{ settings.sortingDirection ? '↓' : '↑' }}
                </button>
            </div>
        </div>
        <div class="option-div">
            <p class="option-title">дата погашения</p>
            <div class="flex flex-col gap-2 bg-neutral-200 p-2">
                <div class="flex flex-row">
                    <p class="pr-2 self-center">от:</p>
                    <flat-pickr class="p-1 self-center" v-model="vueFlatpickrIsStupid.g1" @on-close="(t) => {
                        const selectedDate = t[0];
                        settings.maturityStartDate = new Date(selectedDate.getFullYear(), selectedDate.getMonth(), 0);
                        EmitSettings();
                    }" :config="{
    locale: Russian,
    defaultDate: settings.maturityStartDate,
    minDate: new Date(),
    altInput: true,
    plugins: [
        new monthSelectPlugin({
            shorthand: true
        })
    ]
}">
                    </flat-pickr>
                </div>
                <div class="flex flex-row">
                    <p class="pr-2 self-center">до:</p>
                    <flat-pickr class="p-1 self-center" v-model="vueFlatpickrIsStupid.g2" @on-close="(t) => {
                        const selectedDate = t[0];
                        settings.maturityEndDate = new Date(selectedDate.getFullYear(), selectedDate.getMonth() + 1);
                        EmitSettings();
                    }" :config="{
    locale: Russian,
    defaultDate: settings.maturityEndDate,
    minDate: new Date(),
    plugins: [
        new monthSelectPlugin({
            shorthand: true
        })
    ]
}">
                    </flat-pickr>
                </div>
            </div>
        </div>
        <div class="option-div">
            <div class="flex flex-row-reverse gap-3">
                <button class="border-2 px-1 border-neutral-300 hover:bg-neutral-200 shadow-lg"
                    @click="{settings.couponMonths = settings.couponMonths.map((t) => { return { ...t, active: false }}); EmitSettings();}">
                    𐄂
                </button>
                <button class="border-2 px-1 border-neutral-300 hover:bg-neutral-200 shadow-lg"
                    @click="{settings.couponMonths = settings.couponMonths.map((t) => { return { ...t, active: true } }); EmitSettings();}">
                    ✓
                </button>
                <!--
                <button v-if="!choosingMonthMode" @click="() => { choosingMonthMode = true }"
                    class="ml-auto hover:bg-neutral-200 border-2 px-1 border-neutral-500"> {{
                            settings.couponSelectMode.filter(t =>
                                t.active)[0].name
                    }} </button>
                
                <div class="absolute bg-white ml-auto flex flex-col border-2 border-neutral-500" v-else>
                    <button class="hover:bg-neutral-200 px-1" v-for="couponMode of settings.couponSelectMode" @click="() => {
                        choosingMonthMode = false;
                        settings.couponSelectMode = settings.couponSelectMode.map(t => {
                            const newT = { ...t };
                            if (newT.id == couponMode.id) {
                                newT.active = true;
                            } else {
                                newT.active = false;
                            }
                            return newT;
                        });
                        EmitSettings();
                    }">
                        {{ couponMode.name }}
                    </button>
                </div>
                -->
                <p class="option-title mr-auto">месяцы с купонами</p>
            </div>
            <div class="grid grid-cols-4 grow gap-1">
                <div v-for="month of settings.couponMonths" key="id" class="flex flex-row">
                    <button
                        @click="() => { settings.couponMonths[month.id].active = !settings.couponMonths[month.id].active; EmitSettings() }"
                        class="p-1 basis-1 grow hover:bg-neutral-200 hover:text-black" :class="month.active
                        ? 'text-black border-2 border-neutral-600'
                        : 'border-2 border-neutral-200 text-neutral-500'">
                        {{ month.name }}
                    </button>
                </div>
            </div>
        </div>
        <div class="option-div">
            <div class="flex flex-row-reverse gap-3">
                <button class="border-2 px-1 border-neutral-300 hover:bg-neutral-200 shadow-lg"
                    @click="{settings.sectors = settings.sectors.map((t) => { return { ...t, active: false } }); EmitSettings();}">
                    𐄂
                </button>
                <button class="border-2 px-1 border-neutral-300 hover:bg-neutral-200 shadow-lg"
                    @click="{settings.sectors = settings.sectors.map((t) => { return { ...t, active: true } }); EmitSettings();}">
                    ✓
                </button>
                <p class="option-title mr-auto">секторы</p>
            </div>

            <div class="grid grid-cols-2 gap-1">
                <div v-for="sector of settings.sectors" key="id" class="flex flex-row">
                    <button
                        @click="() => { settings.sectors[sector.id].active = !settings.sectors[sector.id].active; EmitSettings() }"
                        class="p-1 basis-1 grow hover:bg-neutral-200 hover:text-black" :class="sector.active
                        ? 'text-black border-2 border-neutral-600'
                        : 'border-2 border-neutral-200 text-neutral-500'">
                        {{ sector.name }}
                    </button>
                </div>
            </div>

        </div>
    </div>
</template>

<style>
.flatpickr-calendar {
    font-family: roboto;
}

.option-title {
    @apply text-lg
}

.option-div {
    @apply flex flex-col p-1 gap-2
}

.sort-button {
    @apply hover:bg-neutral-200 p-1
}
</style>