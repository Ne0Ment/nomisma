<script setup>
import { ref } from 'vue'
import UpdateToken from './UpdateToken.vue'
import Logout from './Logout.vue';

const emit = defineEmits(['ChangeLoginState']);
</script>

<template>
<div class="flex flex-col flex-wrap gap-4 self-center mt-5">
    <UpdateToken/>
    <Logout @logout="() => emit('ChangeLoginState', false)"/>
</div>
</template>