<script setup>
    import { computed, onBeforeMount, ref } from 'vue'
    import axios from 'axios'
    import Cookies from 'js-cookie';

    const genres = ref([])

    const genreToAdd = ref({})
    const genreToEdit = ref({})

    async function fetchGenres(){
        const r = await axios.get("/api/genres/")
        genres.value = r.data
    }

    async function onGroupAdd(){
        await axios.post("/api/genres/", genreToAdd.value)
        await fetchGenres()
    }

    async function onDeleteClick(genre) {
        await axios.delete(`/api/genres/${genre.id}/`)
        await fetchGenres()
    }

    function onEditClick(genre){
        genreToEdit.value = { ...genre }
    }

    async function onEditSubmitClick(genre) {
        await axios.put(`/api/genres/${genre.id}/`, genreToEdit.value)
        genreToEdit.value = {}
        await fetchGenres()
    }

    function onEditCancelClick(){
        genreToEdit.value = {}
    }

    // Сработает при запуске приложения
    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchGenres()
    })

</script>

<template>
    <div class="p-3">
        <div class="row">
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="genreToAdd.name">
                    <label>Название жанра</label>
                </div>
            </div>
            
            <div class="col-auto mt-auto mb-auto">
                <button class="btn btn-primary" @click="onGroupAdd">
                    <i class="bi bi-plus-square"></i>
                </button>
            </div>
        </div>

        <div v-for="genre in genres">
            <!-- Отображение группы -->
            <div v-if="genre.id != genreToEdit.id" class="item">
                <span>{{ genre.name }}</span>
                <button @click="onEditClick(genre)" class="btn btn-success">
                    <i class="bi bi-pencil-fill"></i>
                </button>
                <button @click="onDeleteClick(genre)" class="btn btn-danger">
                    <i class="bi bi-trash3-fill"></i>
                </button>
            </div>
            <!-- Отображение области редактирования группы -->
            <div v-else>
                <div class="row">
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="genreToEdit.name">
                            <label>Название жанра</label>
                        </div>
                    </div>
                    
                    <div class="col-auto mt-auto mb-auto">
                        <button class="btn btn-success" @click="onEditSubmitClick(genre)">
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
