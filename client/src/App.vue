<script setup>
    import { onBeforeMount } from 'vue';
    import Cookies from 'js-cookie';
    import { storeToRefs } from 'pinia';
    import { useUserStore } from '@/stores/userStore';
    import axios from 'axios';
    import router from './router';

    const userStore = useUserStore()
    const userInfo = storeToRefs(userStore)

    async function logout(){
        await axios.post("/api/user/logout/")
        userStore.getInfo()
        router.push("/login")
    }

    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
    })
</script>

<template>
    <div class="container" v-if="userInfo.isAuthenticated.value">
        <nav class="navbar navbar-expand-lg navbar-light bg-lights">
            <div class="container-fluid">
                <router-link class="navbar-brand" to="/"><i class="bi bi-music-note"></i></router-link>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                    <div class="navbar-nav">
                        <router-link class="nav-link" to="/groups">Группы</router-link>
                        <router-link class="nav-link" to="/members">Участники</router-link>
                        <router-link class="nav-link" to="/albums">Альбомы</router-link>
                        <router-link class="nav-link" to="/songs">Песни</router-link>
                        <router-link class="nav-link" to="/genres">Жанры</router-link>

                        <a v-if="userInfo.isSuperuser" class="nav-link" href="/admin">Админка</a>
                        
                        <ul class="nav-item p-2">
                            <span :class="{'fw-bold': userInfo.isSuperuser}">{{ userInfo.name }}</span>
                            <span class="nav-link d-inline" role="button" @click="logout()">(Выйти)</span> 
                        </ul>
                    </div>
                    
                </div>
            </div>
        </nav>
    </div>

    <div class="container">
	    <router-view/>
    </div>
</template>

<style scoped>

</style>