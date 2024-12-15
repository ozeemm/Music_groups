<script setup>
    import axios from 'axios';
    import Cookies from 'js-cookie';
    import { onBeforeMount, ref } from 'vue';
    import router from '@/router';
    import { storeToRefs } from 'pinia';
    import { useUserStore } from '@/stores/userStore';

    const userStore = useUserStore()
    const userInfo = storeToRefs(userStore)
    
    const loginData = ref({})
    const messageText = ref("")

    async function login() {
        if(!loginData.value.username || !loginData.value.password || loginData.value.username == "" || loginData.value.password == "")
            return
        try{
            await axios.post("/api/user/login/", loginData.value)
            userStore.getInfo()
            axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
            router.push("/") // redirect
            // userStore.getInfo()
            // axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")

        } catch(e){
            messageText.value = "Неверный логин или пароль"
        }
    }

    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
    })
</script>

<template>
    <div style="width: 30%" class="border p-5 mx-auto">
        <div class="mb-4 text-center">
            <h2>Login</h2>
        </div>

        <div class="form-outline mb-3">
            <input type="text" class="form-control" placeholder="Username" v-model="loginData.username" @input="messageText = ''"/>
        </div>

        <div class="form-outline mb-4">
            <input type="password" class="form-control" placeholder="Password" v-model="loginData.password" @input="messageText = ''"/>
        </div>

        <div class="d-flex justify-content-center">
            <button type="submit" class="btn btn-primary mb-3" @click="login()">Sign in</button>
        </div>

        <div class="text-center mb-2">
            <strong class="text-danger">{{ messageText }}</strong>
        </div>

        <div class="text-center">
            <p>Not a member? <a href="/register">Register</a></p>
        </div>
    </div>
</template>

<style></style>