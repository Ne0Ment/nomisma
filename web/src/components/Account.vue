<script setup>
import { ref } from 'vue'
import Cookies from 'js-cookie'

import ControlPanel from './ControlPanel.vue';
import Login from './Login.vue';

const emit = defineEmits(['ToggleLogin']);

const loggedIn = ref(false);
if (Cookies.get('temp-key')) {
    loggedIn.value = true;
}
function ChangeLoginState(newState) {
    loggedIn.value = newState
    emit("ToggleLogin");
}

</script>

<template>
    <ControlPanel v-if="loggedIn" @ChangeLoginState="ChangeLoginState" />
    <Login v-else @ChangeLoginState="ChangeLoginState" />
</template>