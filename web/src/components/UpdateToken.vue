<script setup>
import { ref, reactive } from 'vue'
import Cookies from 'js-cookie'
import StatusDisplay from './StatusDisplay.vue';
import FlashMessage from './FlashMessage.vue';

const emit = defineEmits(['UpdateToken']);

const serverUrl = "";

const newToken = ref('');
const confCode = ref('');
const sendCodeLoadStatus = ref('none');
const confirmLoadStatus = ref('none');

const statusShow = ref(false);
const statusMessage = reactive({ status: false });

const showDropdown = ref(false);

function DisplayStatusMessage(msg) {
    statusMessage.value = msg;
    statusShow.value = true;
    setTimeout(() => {
        statusShow.value = false;
    }, 1500)
}

function FetchConfCode() {
    sendCodeLoadStatus.value = 'loading';
    let tempKey = Cookies.get('temp-key')
    let payload = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ temp_key: tempKey })
    }
    fetch(serverUrl + "/GetConfCode", payload)
        .then(t => t.text())
        .then(t => JSON.parse(t))
        .then(t => {
            sendCodeLoadStatus.value = 'none';
            DisplayStatusMessage(t);
        });
}

function SendNewToken() {
    if (newToken.value != '' && confCode.value != '') {
        emit('UpdateToken', newToken.value);
        confirmLoadStatus.value = 'loading';
        let tempKey = Cookies.get('temp-key')
        let payload = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ temp_key: tempKey, new_token: newToken.value, conf_code: confCode.value })
        }
        fetch(serverUrl + "/SetNewToken", payload)
            .then(t => t.text())
            .then(t => JSON.parse(t))
            .then(t => {
                setTimeout(() => { confirmLoadStatus.value = 'none'; }, 100)
                newToken.value = '';
                confCode.value = '';
                DisplayStatusMessage(t);
            });

    }
}


</script>

<template>
    <div class="flex flex-col bg-neutral-200">
        <FlashMessage :show="statusShow" :passed-message="statusMessage.value" />
            <button class="text-lg m-1 p-2 grow hover:bg-neutral-600 hover:text-white border-neutral-300 rounded-xl"
                    @click="() => {showDropdown = !showDropdown}">обновить токен</button>

        <div class="foldable flex flex-col overflow-hidden"
            :class="{ 'max-h-40': showDropdown, 'max-h-0': !showDropdown }">
            <input v-model="newToken" class="m-1 p-2" placeholder="новый токен">
            <div class="flex flex-row">
                <input v-model="confCode" class="m-1 p-2 grow" placeholder="код подтверждения">
                <StatusDisplay v-if="sendCodeLoadStatus == 'loading'" :load-status="sendCodeLoadStatus" />
                <button v-else @click="FetchConfCode()"
                    class="p-2 mr-1 mb-1 mt-0.5 rounded-xl hover:bg-neutral-600 hover:text-white border-neutral-300 border-2">
                    получить код</button>
            </div>
            <div class="flex flex-row">
                <StatusDisplay v-if="confirmLoadStatus == 'loading'" :load-status="confirmLoadStatus" />
                <button v-else @click="SendNewToken()"
                    class="grow m-1 mb-1.5 p-2 rounded-xl hover:bg-neutral-600 hover:text-white ">отправить</button>
            </div>
        </div>
    </div>
</template>

<style>
.foldable {
    transition: max-height 0.3s ease-in-out;
}
</style>