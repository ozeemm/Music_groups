<script setup>
    import { onBeforeMount, ref, toRaw, useTemplateRef, watch } from 'vue'
    import axios from 'axios'
    import Cookies from 'js-cookie'
    import { storeToRefs } from 'pinia';
    import { useUserStore } from '@/stores/userStore';
    import router from '@/router';
    
    import ImageModal from '@/components/ImageModal.vue'
    import StatsPanel from '@/components/StatsPanel.vue';

    const userStore = useUserStore()
    const userInfo = storeToRefs(userStore)

    const members = ref([])
    const memberImages = ref([])
    const groups = ref([])
    const stats = ref({})

    const memberToAdd = ref({})
    const memberImagesToAdd = ref([])
    const memberAddImageRef = ref()

    const memberToEdit = ref({})
    const memberEditImageRef = ref()

    const imageModalRef = useTemplateRef('imageModalRef')
    const modalImageObj = ref({})

    const isLoading = ref(false)

    // Fetch data
    async function fetchMembers(){
        isLoading.value = true
        const r = await axios.get("/api/members/")
        members.value = r.data
        await fetchMemberImages()
        await fetchStats()
        isLoading.value = false
    }

    async function fetchStats() {
        const r = await axios.get("/api/members/stats/")
        stats.value = r.data
    }

    async function fetchGroups(){
        const r = await axios.get("/api/groups/")
        groups.value = r.data
    }

    async function fetchMemberImages(){
        const r = await axios.get("/api/member_images/")
        memberImages.value = r.data
    }

    // Create
    async function onMemberAdd(){
        const r = await axios.post(`/api/members/`, memberToAdd.value)
        const id = r.data.id

        for(let image of memberImagesToAdd.value){
            const formData = new FormData()
            formData.append('member', id)
            formData.append('image', image.file)

            await axios.post(`/api/member_images/`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
        }

        await fetchMembers()
    }

    function memberAddImageChange(){
        for(let i = 0; i < memberAddImageRef.value.files.length; i++){
            const obj = { file: memberAddImageRef.value.files[i], url: URL.createObjectURL(memberAddImageRef.value.files[i]) }
            memberImagesToAdd.value.push(obj)
        }
    }

    function memberAddImageDelete(index){
        memberImagesToAdd.value.splice(index, 1)
    }
    
    // Edit
    function onEditClick(member){
        memberToEdit.value = { 
            ...member, 
            group: member.group.id,
            images: toRaw(memberImages.value).filter(obj => obj.member == member.id), 
            imagesToAdd: [], 
            imagesToDelete: [] 
        }
    }

    async function onEditSubmitClick() {
        await axios.put(`/api/members/${memberToEdit.value.id}/`, {
            'name': memberToEdit.value.name,
            'role': memberToEdit.value.role,
            'group': memberToEdit.value.group
        })

        for(let id of memberToEdit.value.imagesToDelete){
            await axios.delete(`/api/member_images/${id}/`)
        }
        
        for(let image of memberToEdit.value.imagesToAdd){
            const formData = new FormData()
            formData.append('member', memberToEdit.value.id)
            formData.append('image', image.file)

            await axios.post(`/api/member_images/`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
        }

        memberToEdit.value = {}
        await fetchMembers()
    }

    function onEditCancelClick(){
        memberToEdit.value = {}
    }

    function memberEditImageChange(event){
        for(let i = 0; i < event.target.files.length; i++){
            const obj = { file: event.target.files[i], url: URL.createObjectURL(event.target.files[i]) }
            memberToEdit.value.imagesToAdd.push(obj)
        }
    }

    function memberEditImageDeleteAdded(imageId){
        memberToEdit.value.imagesToAdd.splice(imageId, 1)
    }

    function memberEditImageDeleteExisting(image){
        const index = memberToEdit.value.images.indexOf(image)
        memberToEdit.value.images.splice(index, 1)
        memberToEdit.value.imagesToDelete.push(image.id)
    }

    // Delete
    async function onDeleteClick(member) {
        await axios.delete(`/api/members/${member.id}/`)
        await fetchMembers()
    }
 
    function imageClick(name, imageUrl){
        modalImageObj.value.name = name
        modalImageObj.value.imageUrl = imageUrl

        imageModalRef.value.show()
    }

    // При запуске приложения
    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchMembers()
        await fetchGroups()
    })

    watch(userInfo.isAuthenticated, () => {        
        if(!userInfo.isAuthenticated.value){
            router.push("/login")
            return
        }
    })
</script>

<template>
    <div v-if="isLoading" class="d-flex justify-content-center">
        <div class="spinner-border text-primary" role="status"></div>
    </div>
    <div v-else class="p-3">
        <stats-panel>
            <div class="stats-item col-auto">Всего участников: {{ stats.members_count }}</div>
            <div class="stats-item col-auto">
                <div>Участников по группам:</div>
                <ul>
                    <li v-for="member in stats.members_by_groups">{{ member.group__name }}: {{ member.count }}</li>
                </ul>
            </div>
            <div class="stats-item col-auto">
                <div>Участников по ролям в группе:</div>
                <ul>
                    <li v-for="member in stats.members_by_roles">{{ member.role }}: {{ member.count }}</li>
                </ul>
            </div>
        </stats-panel>

        <div class="row">
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="memberToAdd.name">
                    <label>ФИО</label>
                </div>
            </div>
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="memberToAdd.role">
                    <label>Роль в группе</label>
                </div>
            </div>
            <div class="col-auto">
                <div class="form-floating">
                    <select class="form-select" v-model="memberToAdd.group">
                        <option :value="g.id" v-for="g in groups">{{ g.name }}</option>
                    </select>
                    <label>Группа</label>
                </div>
            </div>
            <div class="col-auto">
                <input class="form-control" type="file" multiple="multiply" ref="memberAddImageRef" @change="memberAddImageChange">
            </div>
            <div class="col-auto mt-auto mb-auto">
                <button class="btn btn-primary" @click="onMemberAdd()">
                    <i class="bi bi-person-plus-fill"></i>
                </button>
            </div>
            <div class="row mt-2">
                <div v-for="(image, index) in memberImagesToAdd" class="col-auto">
                    <img :src="image.url" style="max-height: 60px;" alt="" @click="imageClick(memberToAdd.name, image.url)">
                    <button class="btn btn-danger imageDeleteButton" @click="memberAddImageDelete(index)">
                            <i class="bi bi-x-lg"></i>
                    </button>
                </div>
            </div>
        </div>

        <div v-for="member in members">
            <!-- Отображение -->
            <div v-if="member.id != memberToEdit.id" class="item">
                
                <span>{{ member.name }}</span>
                <span>{{ member.role }}</span> 
                <span>{{ member.group.name }}</span>
                <div v-for="image in memberImages">
                    <img v-if="image.member == member.id" :src="image.image" style="max-height: 60px;" alt="" @click="imageClick(member.name, image.image)">
                </div>
                <span v-if="userInfo.isSuperuser"> Created by {{ member.user.username }} </span>
                <button @click="onEditClick(member)" class="btn btn-success">
                    <i class="bi bi-pencil-fill"></i>
                </button>
                <button @click="onDeleteClick(member)" class="btn btn-danger">
                    <i class="bi bi-person-dash-fill"></i>
                </button>
            </div>
            <!-- Отображение области редактирования участника -->
            <div v-else>
                <div class="row">
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="memberToEdit.name">
                            <label>ФИО</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="memberToEdit.role">
                            <label>Роль в группе</label>
                        </div>
                    </div>
                    <div class="col-auto">
                        <div class="form-floating">
                            <select class="form-select" v-model="memberToEdit.group">
                                <option :value="g.id" v-for="g in groups">{{ g.name }}</option>
                            </select>
                            <label>Группа</label>
                        </div>
                    </div>
                    <div class="col-auto mt-auto mb-auto">
                        <button class="btn btn-success" @click="onEditSubmitClick()">
                            <i class="bi bi-check-lg"></i>
                        </button>
                    </div>
                    <div class="col-auto mt-auto mb-auto">
                        <button class="btn btn-danger" @click="onEditCancelClick()">
                            <i class="bi bi-x-lg"></i>
                        </button>
                    </div>
                </div>

                <div class="row mt-2">
                    <div class="col-auto">
                        <input class="form-control" type="file" multiple="multiply" ref="memberEditImageRef" @change="memberEditImageChange">
                    </div>
                    <div v-for="image in memberToEdit.images" class="col-auto">
                        <img :src="image.image" style="max-height: 60px;" alt="" @click="imageClick(memberToEdit.name, image.image)">
                        <button class="btn btn-danger imageDeleteButton" @click="memberEditImageDeleteExisting(image)">
                                <i class="bi bi-x-lg"></i>
                        </button>
                    </div>
                    <div v-for="(image, index) in memberToEdit.imagesToAdd" class="col-auto">
                        <img :src="image.url" style="max-height: 60px;" alt="" @click="imageClick(memberToEdit.name, image.url)">
                        <button class="btn btn-danger imageDeleteButton" @click="memberEditImageDeleteAdded()">
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
