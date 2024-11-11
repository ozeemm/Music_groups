<script setup>
    import { computed, onBeforeMount, ref } from 'vue'
    import axios from 'axios'
    import Cookies from 'js-cookie';

    const groups = ref([])

    const groupToAdd = ref({})
    const groupToEdit = ref({})

    const userInfo = ref({})

    async function fetchGroups(){
        const r = await axios.get("/api/groups/")
        groups.value = r.data
    }

    async function onGroupAdd(){
        await axios.post("/api/groups/", groupToAdd.value)
        await fetchGroups()
    }

    async function onDeleteClick(group) {
        await axios.delete(`/api/groups/${group.id}/`)
        await fetchGroups()
    }

    function onEditClick(group){
        groupToEdit.value = { ...group }
    }

    async function onEditSubmitClick(group) {
        await axios.put(`/api/groups/${group.id}/`, groupToEdit.value)
        groupToEdit.value = {}
        await fetchGroups()
    }

    function onEditCancelClick(){
        groupToEdit.value = {}
    }

    async function getUserInfo(){
        const r = await axios.get(`/api/user/info/`)
        userInfo.value = r.data
    }

    // Сработает при запуске приложения
    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchGroups()
        await getUserInfo()
    })

</script>

<template>
    {{ userInfo }}
    <div class="p-3">
        <div class="row">
            <div class="col">
                <div class="form-floating">
                    <input type="text" class="form-control" v-model="groupToAdd.name">
                    <label>Название группы</label>
                </div>
            </div>
            
            <div class="col-auto mt-auto mb-auto">
                <button class="btn btn-primary" @click="onGroupAdd">
                    <i class="bi bi-plus-square"></i>
                </button>
            </div>
        </div>

        <div v-for="group in groups">
            <!-- Отображение группы -->
            <div v-if="group.id != groupToEdit.id" class="item">
                <span>{{ group.name }}</span>
                <button @click="onEditClick(group)" class="btn btn-success">
                    <i class="bi bi-pencil-fill"></i>
                </button>
                <button @click="onDeleteClick(group)" class="btn btn-danger">
                    <i class="bi bi-trash3-fill"></i>
                </button>
            </div>
            <!-- Отображение области редактирования группы -->
            <div v-else>
                <div class="row">
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="groupToEdit.name">
                            <label>Название группы</label>
                        </div>
                    </div>
                    
                    <div class="col-auto mt-auto mb-auto">
                        <button class="btn btn-success" @click="onEditSubmitClick(group)">
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
