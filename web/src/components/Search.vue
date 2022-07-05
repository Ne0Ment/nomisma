<script setup>
import { ref, toRef } from 'vue'
import SearchSettings from './searchcomponents/SearchSettings.vue';
import SearchList from './searchcomponents/SearchList.vue';

const props = defineProps({
    bonds: Array
});

const allBonds = toRef(props, 'bonds');

</script>

<template>
    <div class="flex flex-row h-full mt-2 overflow-hidden gap-2">
        <SearchList :all-bonds="allBonds"/>
        <SearchSettings />
    </div>
</template>