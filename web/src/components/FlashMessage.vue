<script setup>
import { watch } from 'vue'
const props = defineProps({
    passedMessage: Object,
    show: Boolean
});
const successClass = "bg-green-400 self-center rounded-b-xl p-3 px-12 transition-transform flex flex-col";
const errorClass = "bg-red-400 self-center rounded-b-xl p-3 px-12 transition-transform flex flex-col";  

</script>

<template>
    <div class="fixed top-0 left-0 right-0 flex flex-col content-center">
        <Transition>
            <div v-if="show==true" :class="passedMessage.status ? successClass : errorClass">
                <p v-if="passedMessage.status" class="text-xl">успех</p>
                <p v-else class="text-xl">ошибка</p>
                <p class="text-lg">{{ passedMessage.error }}</p>
            </div>
        </Transition>
    </div>
</template>

<style>
.v-enter-active,
.v-leave-active {
    transition: all .7s ease-in-out;
}

.v-enter-from,
.v-leave-to {
    transform: translateY(-100%);
}
</style>