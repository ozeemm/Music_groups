<script setup>
    import { onBeforeMount, ref, watch } from 'vue'
    import axios from 'axios'
    import Cookies from 'js-cookie';
    import { storeToRefs } from 'pinia';
    import { useUserStore } from '@/stores/userStore';
    import router from '@/router';

    import StatsPanel from '@/components/StatsPanel.vue';

    const userStore = useUserStore()
    const userInfo = storeToRefs(userStore)

    const genres = ref([])
    const stats = ref({})

    const genreToAdd = ref({})
    const genreToEdit = ref({})

    const isLoading = ref(false)

    async function fetchGenres(){
        isLoading.value = true
        const r = await axios.get("/api/genres/")
        genres.value = r.data
        await fetchStats()
        isLoading.value = false
    }

    async function fetchStats(){
        const r = await axios.get("/api/genres/stats/")
        stats.value = r.data
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
            <div class="stats-item col-auto">Всего жанров: {{ stats.genres_count }}</div>
        </stats-panel>

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
            <!-- Отображение -->
            <div v-if="genre.id != genreToEdit.id" class="item">
                <span>{{ genre.name }}</span>
                <span v-if="userInfo.isSuperuser"> Created by {{ genre.user.username }} </span>
                <div style="justify-content: flex-end;">
                    <button @click="onEditClick(genre)" class="btn btn-success me-2">
                        <i class="bi bi-pencil-fill"></i>
                    </button>
                    <button @click="onDeleteClick(genre)" class="btn btn-danger">
                        <i class="bi bi-trash3-fill"></i>
                    </button>
                </div>
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
