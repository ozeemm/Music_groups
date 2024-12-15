<script setup>
    import axios from 'axios';
    import Cookies from 'js-cookie';
    import { onBeforeMount, ref } from 'vue';
    import router from '@/router';
    import { storeToRefs } from 'pinia';
    import { useUserStore } from '@/stores/userStore';

    const userStore = useUserStore()
    const userInfo = storeToRefs(userStore)
    
    const registerData = ref({})
    const messageText = ref("")

    async function register() {
        if(!registerData.value.username || !registerData.value.password || registerData.value.username == "" || registerData.value.password == "")
            return
        
        try{
            await axios.post("/api/user/register/", registerData.value)
            userStore.getInfo()
            axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
            router.push("/")

        } catch(e){
            messageText.value = "Пользователь уже существует!"
        }
    }

    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
    })
</script>

<template>
    <div style="width: 30%" class="border p-5 mx-auto">
        <div class="mb-4 text-center">
            <h2>Register</h2>
        </div>

        <div class="form-outline mb-3">
            <input type="text" class="form-control" placeholder="Username" v-model="registerData.username" @input="messageText = ''"/>
        </div>

        <div class="form-outline mb-3">
            <input type="email" class="form-control" placeholder="Email" v-model="registerData.email" @input="messageText = ''"/>
        </div>

        <div class="form-outline mb-4">
            <input type="password" class="form-control" placeholder="Password" v-model="registerData.password" @input="messageText = ''"/>
        </div>

        <div class="d-flex justify-content-center">
            <button type="submit" class="btn btn-primary mb-3" @click="register()">Sign up</button>
        </div>

        <div class="text-center mb-2">
            <strong class="text-danger">{{ messageText }}</strong>
        </div>
        
        <div class="text-center">
            <p>Have account? <a href="/login">Login</a></p>
        </div>
    </div>
</template>

<style>

</style>