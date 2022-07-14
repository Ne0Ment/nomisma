<script setup>
import { ref } from 'vue'
import Cookies from 'js-cookie'
import TelegramLogin from './TelegramLogin.vue'

const emit = defineEmits(['ChangeLoginState']);

const serverUrl = "";

function HandleLogin(user) {
    let payload = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user)
    }
    fetch(serverUrl + "/Login", payload)
        .then(t => t.text())
        .then(t => JSON.parse(t))
        .then(t => {
            if (t.status) {
                Cookies.set('temp-key', t.temp_key)
                emit("ChangeLoginState", true);
            } else {
                console.log('Something went wrong while logging in')
            }
        })
}
</script>

<template>
    <div class="self-center w-1/3">
        <div class="flex flex-col h-1/3">
            <h1 class="self-center text-2xl my-5">вход/регистрация</h1>
            <TelegramLogin class="self-center bg-neutral-300 p-4 rounded-xl" mode="callback"
                telegram-login="Nomisma_Login_Bot" @callback="HandleLogin" requestAccess="write" />
            <!--
        <div class="bg-neutral-200 flex flex-col border-neutral-200 border-4">
            
            <input v-model="loginUsername" @keyup.enter.native="loginPassField.focus()" class="inputfield" placeholder="@telegram"/>
            <input ref="loginPassField" v-model="loginPass" @keyup.enter.native="SendLogin()" type=password class="inputfield" placeholder="password"/>
            <button @click="SendLogin()" class="formbutton">It's me</button>
        </div>
        -->
        </div>
    </div>
</template>