<script setup>
    import { onBeforeMount, ref, useTemplateRef, watch } from 'vue'
    import axios from 'axios'
    import Cookies from 'js-cookie';
    import { storeToRefs } from 'pinia';
    import { useUserStore } from '@/stores/userStore';
    import router from '@/router';
    
    import ImageModal from '@/components/ImageModal.vue';
    import StatsPanel from '@/components/StatsPanel.vue';

    const userStore = useUserStore()
    const userInfo = storeToRefs(userStore)

    const albums = ref([])
    const groups = ref([])
    const genres = ref([])
    const stats = ref({})

    const albumToAdd = ref({})
    const albumToAddImageFile = ref(null)
    const albumToEdit = ref({})
    const albumToEditImageFile = ref(null)

    const albumImageRef = ref()
    const albumEditImageRef = ref() // Тут будет массив, так как input создаётся в for

    const imageModalRef = useTemplateRef('imageModalRef')
    const modalImageObj = ref({})

    const isLoading = ref(false)

    async function fetchAlbums(){
        isLoading.value = true
        const r = await axios.get("/api/albums/")
        albums.value = r.data
        await fetchStats()
        isLoading.value = false
    }

    async function fetchStats(){
        const r = await axios.get("/api/albums/stats/")
        stats.value = r.data
    }

    async function fetchGroups(){
        const r = await axios.get("/api/groups/")
        groups.value = r.data
    }

    async function fetchGenres(){
        const r = await axios.get("/api/genres/")
        genres.value = r.data
    }

    async function onAlbumAdd(){
        const formData = new FormData()

        // "Введённый" файл
        if(albumToAddImageFile.value != null)
            formData.append('image', albumToAddImageFile.value)

        formData.set('name', albumToAdd.value.name)
        formData.set('year', albumToAdd.value.year)
        formData.set('group', albumToAdd.value.group)
        formData.set('genre', albumToAdd.value.genre)

        // Указываем в заголовке, что отправляем данные с файлом
        await axios.post("/api/albums/", formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
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
            genre: album.genre.id,
        }
    }

    async function onEditSubmitClick(album) {
        const formData = new FormData()
        
        // "Введённый" файл
        if(albumToEditImageFile.value){ // Image changed
            formData.append('image', albumToEditImageFile.value)
        }
        else if(album.image != albumToEdit.value.image) // Image deleted        
            formData.append('image', "")

        formData.set('name', albumToEdit.value.name)
        formData.set('year', albumToEdit.value.year)
        formData.set('group', albumToEdit.value.group)
        formData.set('genre', albumToEdit.value.genre)

        // Указываем в заголовке, что отправляем данные с файлом
        await axios.put(`/api/albums/${album.id}/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })

        albumToEdit.value = {}
        albumToEditImageFile.value = null

        await fetchAlbums()
    }

    function onEditCancelClick(){
        albumToEdit.value = {}
        albumToEditImageFile.value = null
    }

    function albumAddImageChange(){
        albumToAddImageFile.value = albumImageRef.value.files[0]
        albumToAdd.value.image = URL.createObjectURL(albumImageRef.value.files[0])
    }

    function albumAddImageDelete(){
        albumToAddImageFile.value = null
        albumToAdd.value.image = null
    }
    
    function albumEditImageChange(event){
        albumToEditImageFile.value = event.target.files[0]
        albumToEdit.value.image = URL.createObjectURL(event.target.files[0])
    }

    function albumEditImageDelete(){
        albumToEditImageFile.value = null
        albumToEdit.value.image = null
    }

    function imageClick(album){
        modalImageObj.value.name = album.name
        modalImageObj.value.imageUrl = album.image
        
        imageModalRef.value.show()
    }

    // Сработает при запуске приложения
    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchAlbums()
        await fetchGroups()
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
            <div class="stats-item col-auto">Всего альбомов: {{ stats.albums_count }}</div>
            <div class="col-auto">
                <div class="stats-item">Самый старый альбом: {{ stats.oldest_album_year }}</div>
                <div class="stats-item">Самый новый альбом: {{ stats.newest_album_year }}</div>
            </div>
            <div class="stats-item col-auto">
                <div>Альбомов по группам:</div>
                <ul>
                    <li v-for="album in stats.albums_by_groups">{{ album.group__name }}: {{ album.count }}</li>
                </ul>
            </div>
            <div class="stats-item col-auto">
                <div>Альбомов по жанрам:</div>
                <ul>
                    <li v-for="album in stats.albums_by_genres">{{ album.genre__name }}: {{ album.count }}</li>
                </ul>
            </div>
            <div class="stats-item col-auto">
                <div>Альбомов по годам:</div>
                <ul>
                    <li v-for="album in stats.albums_by_years">{{ album.year }}: {{ album.count }}</li>
                </ul>
            </div>
        </stats-panel>

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
            <div class="col-auto">
                <input class="form-control" type="file" ref="albumImageRef" @change="albumAddImageChange">
            </div>
            <div class="col-auto">
                <img :src="albumToAdd.image" style="max-height: 60px;" alt="" @click="imageClick(albumToAdd)">
                <button v-if="albumToAdd.image" class="btn btn-danger imageDeleteButton" @click="albumAddImageDelete()">
                    <i class="bi bi-x-lg"></i>
                </button>
            </div>

            <div class="col-auto mt-auto mb-auto">
                <button class="btn btn-primary" @click="onAlbumAdd()">
                    <i class="bi bi-plus-square"></i>
                </button>
            </div>
        </div>

        <div v-for="album in albums">
            <!-- Отображение -->
            <div v-if="album.id != albumToEdit.id" class="item">
                <span v-if="album.image" v-show="album.image">
                    <img :src="album.image" style="max-height: 60px" @click="imageClick(album)">
                </span>
                <span>{{ album.name }}</span>
                <span>{{ album.year }}</span> 
                <span>{{ album.group.name }}</span>
                <span>{{ album.genre.name }}</span>
                <span v-if="userInfo.isSuperuser"> Created by {{ album.user.username }} </span>
                <div style="justify-content: flex-end;">
                    <button @click="onEditClick(album)" class="btn btn-success me-2">
                        <i class="bi bi-pencil-fill"></i>
                    </button>
                    <button @click="onDeleteClick(album)" class="btn btn-danger">
                        <i class="bi bi-trash3-fill"></i>
                    </button>
                </div>
            </div>
            <!-- Отображение области редактирования альбома -->
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

                    <div class="col-auto">
                        <input class="form-control" type="file" @change="albumEditImageChange">
                    </div>
                    <div class="col-auto">
                        <img :src="albumToEdit.image" style="max-height: 60px;" alt="" @click="imageClick(albumToEdit)">
                        <button v-if="albumToEdit.image" class="btn btn-danger imageDeleteButton" @click="albumEditImageDelete()">
                            <i class="bi bi-x-lg"></i>
                        </button>
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

        <image-modal :title="modalImageObj.name" :image="modalImageObj.imageUrl" ref="imageModalRef"/>
    </div>
</template>

<style scoped>
.imageDeleteButton{
    position: relative;
    top: -25px;
    right: 25px;
    transform: scale(0.6);
}
</style>
