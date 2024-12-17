<script setup>
    import { onBeforeMount, ref, computed, watch } from 'vue'
    import axios from 'axios'
    import Cookies from 'js-cookie';
    import { storeToRefs } from 'pinia';
    import { useUserStore } from '@/stores/userStore';
    import router from '@/router';

    import StatsPanel from '@/components/StatsPanel.vue';

    const userStore = useUserStore()
    const userInfo = storeToRefs(userStore)

    const songs = ref([])
    const albums = ref([])
    const stats = ref({})

    const songToAdd = ref({})
    const songToEdit = ref({})

    const isLoading = ref(false)

    // const users = computed(() => new Set(songs.value.map(song => song.user.username)))
    // const songsFiltered = computed(() => songs.value.filter(song => song.name == "Миграция"))
    
    async function fetchSongs(){
        isLoading.value = true
        const r = await axios.get("/api/songs/")
        songs.value = r.data
        await fetchStats()
        isLoading.value = false
    }

    async function fetchStats(){
        const r = await axios.get("/api/songs/stats/")
        stats.value = r.data
    }

    async function fetchAlbums(){
        const r = await axios.get("/api/albums/")
        albums.value = r.data
    }

    async function onAlbumAdd(){
        await axios.post("/api/songs/", songToAdd.value)
        await fetchSongs()
    }

    async function onDeleteClick(song) {
        await axios.delete(`/api/songs/${song.id}/`)
        await fetchSongs()
    }

    function onEditClick(song){
        songToEdit.value = { ...song, album: song.album.id }
    }

    async function onEditSubmitClick(song) {
        await axios.put(`/api/songs/${song.id}/`, songToEdit.value)
        songToEdit.value = {}
        await fetchSongs()
    }

    function onEditCancelClick(){
        songToEdit.value = {}
    }

    // Сработает при запуске приложения
    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchSongs()
        await fetchAlbums()
    })

    watch(userInfo.isAuthenticated, () => {        
        if(!userInfo.isAuthenticated.value){
            router.push("/login")
        }
    })

</script>

<template>
    <div v-if="isLoading" class="d-flex justify-content-center">
        <div class="spinner-border text-primary" role="status"></div>
    </div>
    <div v-else class="p-3">
        <stats-panel>
            <div class="stats-item col-auto">Всего песен: {{ stats.songs_count }}</div>
            <div class="stats-item col-auto">
                <div>Песен по альбомам:</div>
                <ul>
                    <li v-for="song in stats.songs_by_albums">{{ song.album__name }}: {{ song.count }}</li>
                </ul>
            </div>
        </stats-panel>

        <div class="row">
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="songToAdd.name">
                    <label>Название песни</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="songToAdd.album">
                        <option :value="a.id" v-for="a in albums">{{ a.name }}</option>
                    </select>
                    <label>Альбом</label>
                </div>
            </div>
            
            <div class="col-auto mt-auto mb-auto">
                <button class="btn btn-primary" @click="onAlbumAdd">
                    <i class="bi bi-plus-square"></i>
                </button>
            </div>
        </div>

        <div v-for="song in songs">
            <!-- Отображение -->
            <div v-if="song.id != songToEdit.id" class="item">
                <span>{{ song.name }}</span>
                <span>{{ song.album.name }}</span>
                <span v-if="userInfo.isSuperuser"> Created by {{ song.user.username }} </span>
                <div style="justify-content: flex-end;">
                    <button @click="onEditClick(song)" class="btn btn-success me-2">
                        <i class="bi bi-pencil-fill"></i>
                    </button>
                    <button @click="onDeleteClick(song)" class="btn btn-danger">
                        <i class="bi bi-trash3-fill"></i>
                    </button>
                </div>
            </div>
            <!-- Отображение области редактирования группы -->
            <div v-else>
                <div class="row">
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="songToEdit.name">
                            <label>Название песни</label>
                        </div>
                    </div>
                    <div class="col-auto">
                        <div class="form-floating">
                            <select class="form-select" v-model="songToEdit.album">
                                <option :value="a.id" v-for="a in albums">{{ a.name }}</option>
                            </select>
                            <label>Альбом</label>
                        </div>
                    </div>
                    
                    <div class="col-auto mt-auto mb-auto">
                        <button class="btn btn-success" @click="onEditSubmitClick(song)">
                            <i class="bi bi-check-lg"></i>
                        </button>
                    </div>
                    <div class="col-auto mt-auto mb-auto">
                        <button class="btn btn-danger" @click="onEditCancelClick()">
                            <i class="bi bi-x-lg"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>
