<script setup>
    import Cookies from 'js-cookie'
    const emit = defineEmits(['logout']);

    function Logout() {
        Cookies.set('temp-key', '');
        emit('logout');
    }
</script>

<template>
    <div class="flex flex-col bg-neutral-200">
        <button 
            @click="Logout()"
            class="m-1 p-2 rounded-xl hover:bg-neutral-600 hover:text-white text-lg">
            выйти
        </button>
    </div>
</template>