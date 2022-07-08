<script setup>
import { ref, onMounted } from 'vue';

const emit = defineEmits(['UpdateSettings']);

const settings = ref([
    { name: 'налог', valueName: 'tax', value: true },
    { name: 'купоны', valueName: 'coupons', value: true },
    { name: 'погашения', valueName: 'repayments', value: false }
]);

function EmitSettings() {
    let emitSettings = {};
    for (const setting of settings.value) {
        emitSettings[setting.valueName] = setting.value;
    }
    emit('UpdateSettings', emitSettings);
}
onMounted(() => {
    EmitSettings();
});

</script>

<template>
    <div class="flex flex-col gap-2 ml-2">
        <h1 class="text-lg">настройки</h1>
        <div class="flex flex-row px-2 py-1 bg-neutral-200" v-for="setting in settings">
            <input class="w-6 h-6" type="checkbox" id="checkbox" v-model="setting.value" @change="EmitSettings" />
            <button class="grow px-2 flex flex-row">
                <p>{{ setting.name }}</p>
            </button>
        </div>
    </div>
</template>