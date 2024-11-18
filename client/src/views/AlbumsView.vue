<script setup>
    import { onBeforeMount, ref, useTemplateRef } from 'vue'
    import axios from 'axios'
    import Cookies from 'js-cookie';

    import ImageModal from '@/components/ImageModal.vue';

    const albums = ref([])
    const groups = ref([])
    const genres = ref([])

    const albumToAdd = ref({})
    const albumToEdit = ref({})

    const albumImageRef = ref()
    const albumEditImageRef = ref() // Тут будет массив, так как input создаётся в for

    const imageModalRef = useTemplateRef('imageModalRef')
    const modalImageObj = ref({})

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

    async function onAlbumAdd(){
        const formData = new FormData()

        // "Введённый" файл
        if(albumImageRef.value.files[0] != null)
            formData.append('image', albumImageRef.value.files[0])

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
            genre: album.genre.id
        }
    }

    async function onEditSubmitClick(album) {
        const formData = new FormData()

        // "Введённый" файл
        if(albumEditImageRef.value != null)
            formData.append('image', albumEditImageRef.value.files[0])

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
        await fetchAlbums()
    }

    function onEditCancelClick(){
        albumToEdit.value = {}
        albumEditImageRef.value = null
    }

    async function albumAddImageChange(){
        albumToAdd.value.image = URL.createObjectURL(albumImageRef.value.files[0])
    }
    
    async function albumEditImageChange(event){
        albumEditImageRef.value.files = event.target.files
        albumToEdit.value.image = URL.createObjectURL(albumEditImageRef.value[0].files[0])
    }

    // Сработает при запуске приложения
    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchAlbums()
        await fetchGroups()
        await fetchGenres()
    })

    function imageClick(album){
        modalImageObj.value.name = album.name
        modalImageObj.value.imageUrl = album.image
        
        imageModalRef.value.show()
    }

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
            <div class="col-auto">
                <input class="form-control" type="file" ref="albumImageRef" @change="albumAddImageChange">
            </div>
            <div class="col-auto">
                <img :src="albumToAdd.image" style="max-height: 60px;" alt="" @click="imageClick(albumToAdd)">
            </div>

            <div class="col-auto mt-auto mb-auto">
                <button class="btn btn-primary" @click="onAlbumAdd()">
                    <i class="bi bi-plus-square"></i>
                </button>
            </div>
        </div>

        <div v-for="album in albums">
            <!-- Отображение альбомов -->
            <div v-if="album.id != albumToEdit.id" class="item">
                <span>{{ album.name }}</span>
                <span>{{ album.year }}</span> 
                <span>{{ album.group.name }}</span>
                <span>{{ album.genre.name }}</span>
                <span v-if="album.image" v-show="album.image">
                    <img :src="album.image" style="max-height: 60px" @click="imageClick(album)">
                </span>
                <button @click="onEditClick(album)" class="btn btn-success">
                    <i class="bi bi-pencil-fill"></i>
                </button>
                <button @click="onDeleteClick(album)" class="btn btn-danger">
                    <i class="bi bi-trash3-fill"></i>
                </button>
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
</style>
