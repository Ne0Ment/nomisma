<script setup>
import { ref, toRef, computed } from 'vue'
import SearchSettings from './searchcomponents/SearchSettings.vue';
import SearchList from './searchcomponents/SearchList.vue';
import SearchBar from './searchcomponents/SearchBar.vue';

const props = defineProps({
    bonds: Array
});

const allBonds = toRef(props, 'bonds');
const searchSettings = ref(null);
const searchBar = ref('');

const searchResults = computed(() => {
    
});

function UpdateSettings(settings) {
    searchSettings.value = settings;
}

function UpdateSearchbar(val) {
    searchBar.value = val;
}
</script>

<template>
    <div class="flex flex-row h-full mt-2 overflow-hidden gap-2">
        <div class="flex flex-col grow">
            <SearchBar @update-search="UpdateSearchbar" />
            <SearchList :all-bonds="allBonds" />
        </div>
        <div class="flex flex-col">
            <SearchSettings @update-settings="UpdateSettings" />
        </div>
    </div>
</template>