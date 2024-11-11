<script setup>
    import { computed, onBeforeMount, ref, toRaw } from 'vue'
    import axios from 'axios'
    import Cookies from 'js-cookie';

    const members = ref([])
    const memberImages = ref([])
    const groups = ref([])

    const memberToAdd = ref({})
    const memberImagesToAdd = ref([])
    const memberAddImageRef = ref()
    const memberToEdit = ref({})
    const memberImagesToEdit = ref({})

    async function fetchMembers(){
        const r = await axios.get("/api/members/")
        members.value = r.data

    }

    async function fetchGroups(){
        const r = await axios.get("/api/groups/")
        groups.value = r.data
        await fetchMemberImages()
    }

    async function fetchMemberImages(){
        const r = await axios.get("/api/member_images/")
        memberImages.value = r.data
    }

    async function onMemberAdd(){
        const formData = new FormData()
        for(let i = 0; i < memberImagesToAdd.value.length; i++){
            formData.append(`image[${i}]`, memberImagesToAdd.value[i].file)
        }

        formData.append('name', memberToAdd.value["name"])
        formData.append('role', memberToAdd.value["role"])
        formData.append('group', memberToAdd.value["group"])
        
        for (var pair of formData.entries()) {
            console.log(pair[0]+ ', ' + pair[1]); 
        }

        await axios.post(`/api/members/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })

        await fetchMembers()
    }

    async function onDeleteClick(member) {
        await axios.delete(`/api/members/${member.id}/`)
        await fetchMembers()
    }

    function onEditClick(member){
        memberToEdit.value = { ...member, group: member.group.id }
    }

    async function onEditSubmitClick(member) {
        await axios.put(`/api/members/${member.id}/`, memberToEdit.value)
        memberToEdit.value = {}
        await fetchMembers()
    }

    function onEditCancelClick(){
        memberToEdit.value = {}
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

    function memberImagesById(id){
        return toRaw(memberImages.value).filter(obj => obj.member == id)
    }

    function imageClick(){
        console.log(`Clicked on image`)
    }

    // Сработает при запуске приложения
    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchMembers()
        await fetchGroups()
    })

</script>

<template>
    <div class="p-3">
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
                    <img :src="image.url" style="max-height: 60px;" alt="" @click="imageClick()">
                    <button class="btn btn-danger imageDeleteButton" @click="memberAddImageDelete(index)">
                            <i class="bi bi-x-lg"></i>
                    </button>
                </div>
            </div>
        </div>

        <div v-for="member in members">
            <!-- Отображение участников -->
            <div v-if="member.id != memberToEdit.id" class="item">
                
                <span>{{ member.name }}</span>
                <span>{{ member.role }}</span> 
                <span>{{ member.group.name }}</span>
                <div v-for="image in memberImages">
                    <img v-if="image.member == member.id" :src="image.image" style="max-height: 60px;" alt="" @click="imageClick()">
                </div>
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
                        <button class="btn btn-success" @click="onEditSubmitClick(member)">
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
.imageDeleteButton{
    position: relative;
    top: -25px;
    right: 25px;
    transform: scale(0.6);
}
</style>
