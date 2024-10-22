<script setup>
    import { computed, onBeforeMount, ref } from 'vue'
    import axios from 'axios'
    import Cookies from 'js-cookie';

    const albums = ref([])
    const groups = ref([])
    const genres = ref([])

    const albumToAdd = ref({})
    const albumToEdit = ref({})

    async function fetchAlbums(){
        const r = await axios.get("/api/albums/")
        albums.value = r.data
    }

    async function fetchGroups(){
        const r = await axios.get("/api/groups/")
        groups.value = r.data
    }

    async function fetchGenres(){
        const r = await axios.get("/api/genres/")
        genres.value = r.data
    }

    async function onLoadClick(){
        await fetchAlbums()
    }

    async function onAlbumAdd(){
        await axios.post("/api/albums/", albumToAdd.value)
        await fetchAlbums()
    }

    async function onDeleteClick(album) {
        await axios.delete(`/api/albums/${album.id}/`)
        await fetchAlbums()
    }

    function onEditClick(album){
        albumToEdit.value = { 
            ...album, 
            group: album.group.id, 
            genre: album.genre.id 
        }
    }

    async function onEditSubmitClick(album) {
        await axios.put(`/api/albums/${album.id}/`, albumToEdit.value)
        albumToEdit.value = {}
        await fetchAlbums()
    }

    function onEditCancelClick(){
        albumToEdit.value = {}
    }

    // Сработает при запуске приложения
    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchAlbums()
        await fetchGroups()
        await fetchGenres()
    })

</script>

<template>
    <div class="p-3">
        <div class="row">
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="albumToAdd.name">
                    <label>Название альбома</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                    <input type="number" class="form-control" v-model="albumToAdd.year">
                    <label>Год выпуска</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="albumToAdd.group">
                        <option :value="g.id" v-for="g in groups">{{ g.name }}</option>
                    </select>
                    <label>Группа</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="albumToAdd.genre">
                        <option :value="g.id" v-for="g in genres">{{ g.name }}</option>
                    </select>
                    <label>Жанр</label>
                </div>
            </div>
            <div class="col-auto mt-auto mb-auto">
                <button class="btn btn-primary" @click="onAlbumAdd()">
                    <i class="bi bi-plus-square"></i>
                </button>
            </div>
        </div>

        <div v-for="album in albums">
            <!-- Отображение участников -->
            <div v-if="album.id != albumToEdit.id" class="item">
                <span>{{ album.name }}</span>
                <span>{{ album.year }}</span> 
                <span>{{ album.group.name }}</span>
                <span>{{ album.genre.name }}</span>
                <button @click="onEditClick(album)" class="btn btn-success">
                    <i class="bi bi-pencil-fill"></i>
                </button>
                <button @click="onDeleteClick(album)" class="btn btn-danger">
                    <i class="bi bi-trash3-fill"></i>
                </button>
            </div>
            <!-- Отображение области редактирования участника -->
            <div v-else>
                <div class="row">
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="albumToEdit.name">
                            <label>Название альбома</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input type="number" class="form-control" v-model="albumToEdit.year">
                            <label>Год выпуска</label>
                        </div>
                    </div>
                    <div class="col-auto">
                        <div class="form-floating">
                            <select class="form-select" v-model="albumToEdit.group">
                                <option :value="g.id" v-for="g in groups">{{ g.name }}</option>
                            </select>
                            <label>Группа</label>
                        </div>
                    </div>
                    <div class="col-auto">
                        <div class="form-floating">
                            <select class="form-select" v-model="albumToEdit.genre">
                                <option :value="g.id" v-for="g in genres">{{ g.name }}</option>
                            </select>
                            <label>Жанр</label>
                        </div>
                    </div>
                    <div class="col-auto mt-auto mb-auto">
                        <button class="btn btn-success" @click="onEditSubmitClick(album)">
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
