<script setup>
    import { onBeforeMount, ref, watch } from 'vue';
    import axios from 'axios';
    import Cookies from 'js-cookie';
    import { storeToRefs } from 'pinia';
    import { useUserStore } from '@/stores/userStore';
    import router from '@/router';

    const userStore = useUserStore()
    const userInfo = storeToRefs(userStore)

    const stats = ref({})
    const isLoading = ref(false)

    async function fetchStats(){
        let r = await axios.get("/api/groups/stats/")
        stats.value.groups_count = r.data.groups_count

        r = await axios.get("/api/members/stats/")
        stats.value.members_count = r.data.members_count

        r = await axios.get("/api/albums/stats/")
        stats.value.albums_count = r.data.albums_count

        r = await axios.get("/api/songs/stats/")
        stats.value.songs_count = r.data.songs_count

        r = await axios.get("/api/genres/stats/")
        stats.value.genres_count = r.data.genres_count
    }

    onBeforeMount(async () => {
        if(!userInfo.isAuthenticated.value){
            router.push("/login")
            return
        }

        isLoading.value = true
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchStats()
        isLoading.value = false
    })

</script>

<template>
    <div v-if="isLoading" class="d-flex justify-content-center">
        <div class="spinner-border text-primary" role="status"></div>
    </div>
    <div v-else class="p-3">
        <h2>Добро пожаловать!</h2>
        <div class="list-group py-3">
            <a href="/groups" class="list-group-item list-group-item-action">Группы({{ stats.groups_count }})</a>
            <a href="/members" class="list-group-item list-group-item-action">Участники({{ stats.members_count }})</a>
            <a href="/albums" class="list-group-item list-group-item-action">Альбомы({{ stats.albums_count }})</a>
            <a href="/songs" class="list-group-item list-group-item-action">Песни({{ stats.songs_count }})</a>
            <a href="/genres" class="list-group-item list-group-item-action">Жанры({{ stats.genres_count }})</a>
        </div>
        <a v-if="userInfo.isSuperuser.value" type="button" class="btn btn-success" href="/api/export/xlsx/">Export in xlsx</a>
    </div>
</template>