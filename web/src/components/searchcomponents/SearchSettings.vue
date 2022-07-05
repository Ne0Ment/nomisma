<script setup>
import { reactive } from 'vue';

import flatPickr from 'vue-flatpickr-component';
import 'flatpickr/dist/flatpickr.css';
import monthSelectPlugin from 'flatpickr/dist/plugins/monthSelect/index.js'
import 'flatpickr/dist/plugins/monthSelect/style.css'
import { Russian } from "flatpickr/dist/l10n/ru.js"

function AddYears(date, yearCount) {
    date.setFullYear(date.getFullYear() + yearCount)
    return date;
}

const props = defineProps({
    allBonds: Array
});

const settings = reactive({
    maturityStartDate: AddYears(new Date(), 1),
    maturityEndDate: AddYears(new Date(), 2),
    couponMonths: [
        { 'name': 'янв', active: true, id: 0 },
        { 'name': 'фер', active: true, id: 1 },
        { 'name': 'март', active: true, id: 2 },
        { 'name': 'апр', active: true, id: 3 },
        { 'name': 'май', active: true, id: 4 },
        { 'name': 'июнь', active: true, id: 5 },
        { 'name': 'июль', active: true, id: 6 },
        { 'name': 'авг', active: true, id: 7 },
        { 'name': 'сен', active: true, id: 8 },
        { 'name': 'окт', active: true, id: 9 },
        { 'name': 'ноя', active: true, id: 10 },
        { 'name': 'дек', active: true, id: 11 },
    ]
});
</script>

<template>
    <div class="flex flex-col gap-2">
        <div class="option-div">
            <p class="option-title">дата погашения</p>
            <div class="flex flex-col gap-2 bg-neutral-200 p-2">
                <div class="flex flex-row">
                    <p class="pr-2 self-center">от:</p>
                    <flat-pickr class="p-1 rounded-md self-center" v-model="settings.maturityStartDate" :config="{
                        locale: Russian,
                        minDate: new Date(),
                        plugins: [
                            new monthSelectPlugin({
                                shorthand: true
                            })
                        ]
                    }"></flat-pickr>
                </div>
                <div class="flex flex-row">
                    <p class="pr-2 self-center">до:</p>
                    <flat-pickr class="p-1 rounded-md self-center" v-model="settings.maturityEndDate" :config="{
                        locale: Russian,
                        minDate: new Date(),
                        plugins: [
                            new monthSelectPlugin({
                                shorthand: true
                            })
                        ]
                    }"></flat-pickr>
                </div>
            </div>
        </div>
        <div class="option-div">
            <p class="option-title">месяцы с купонами</p>
            <div class="flex flex-row bg-neutral-200 p-2.5">
                <div class="flex flex-col grow gap-1 m-auto">
                    <div v-for="month of settings.couponMonths.slice(0, 6)" key="id" class="flex flex-row gap-1.5">
                        <input type="checkbox" class="h-5 w-5" v-model="month.active" />
                        <p class="self-center"> {{ month.name }} </p>
                    </div>
                </div>
                <div class="flex flex-col grow gap-1 m-auto">
                    <div v-for="month of settings.couponMonths.slice(6)" key="id" class="flex flex-row gap-1.5">
                        <input type="checkbox" class="h-5 w-5" v-model="month.active" />
                        <p class="self-center"> {{ month.name }} </p>
                    </div>
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
    @apply flex flex-col p-2 gap-2 pl-2
}
</style>