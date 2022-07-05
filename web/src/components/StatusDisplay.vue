<script setup>
import { ref } from 'vue'
import { TrinityRingsSpinner } from 'epic-spinners'

const props = defineProps({
    loadStatus: String,
});

</script>

<template class="self-center">
<trinity-rings-spinner
        class="self-center p-0"
        v-if="loadStatus=='loading'"
        :animation-duration="1000"
        :size="50"
        color="#525252"
        />
</template>