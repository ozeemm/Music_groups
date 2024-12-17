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

    const groups = ref([])
    const stats = ref({})

    const groupToAdd = ref({})
    const groupToEdit = ref({})

    const isLoading = ref(false)

    async function fetchGroups(){
        isLoading.value = true
        const r = await axios.get("/api/groups/")
        groups.value = r.data
        await fetchStats()
        isLoading.value = false
    }

    async function fetchStats(){
        const r = await axios.get("/api/groups/stats/")
        stats.value = r.data
    }

    async function onGroupAdd(){
        await axios.post("/api/groups/", groupToAdd.value)
        await fetchGroups()
        groupToAdd.value = {}
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

    // Сработает при запуске приложения
    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchGroups()
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
            <div class="stats-item col-auto">Всего групп: {{ stats.groups_count }}</div>
        </stats-panel>

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
            <!-- Отображение -->
            <div v-if="group.id != groupToEdit.id" class="item">
                <span>{{ group.name }}</span>
                <span v-if="userInfo.isSuperuser"> Created by {{ group.user.username }} </span>
                <div style="justify-content: flex-end;">
                    <button @click="onEditClick(group)" class="btn btn-success me-2">
                        <i class="bi bi-pencil-fill"></i>
                    </button>
                    <button @click="onDeleteClick(group)" class="btn btn-danger">
                        <i class="bi bi-trash3-fill"></i>
                    </button>
                </div>
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
