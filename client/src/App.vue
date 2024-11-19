<script setup>
    import { storeToRefs } from 'pinia';
    import { useUserStore } from '@/stores/userStore';

    const userStore = useUserStore()
    const userInfo = storeToRefs(userStore)
</script>

<template>
    <div class="container">
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
                        <div class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                Пользователь
                            </a>
                            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                                <li><a class="dropdown-item" href="/admin">Админка</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    </div>
    <div class="container">
        {{ userInfo }}
	    <router-view/>
    </div>
</template>

<style scoped>

</style>