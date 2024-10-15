<script setup>
    import { computed, onBeforeMount, ref } from 'vue'
    import axios from 'axios'
    import Cookies from 'js-cookie';

    const members = ref([])
    const groups = ref([])

    const memberToAdd = ref({})
    const memberToEdit = ref({})

    async function fetchMembers(){
        const r = await axios.get("/api/members/")
        members.value = r.data
    }

    async function fetchGroups(){
        const r = await axios.get("/api/groups/")
        groups.value = r.data
    }

    async function onLoadClick(){
        await fetchMembers()
    }

    async function onMemberAdd(){
        await axios.post("/api/members/", memberToAdd.value)
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

    // Сработает при запуске приложения
    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchMembers()
        await fetchGroups()
    })

</script>

<template>
    <div class="p-3">
        memberToAdd: {{ memberToAdd }}<br>
        memberToEdit: {{ memberToEdit }}
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
                <button class="btn btn-primary" @click="onMemberAdd(item)">
                    <i class="bi bi-person-plus-fill"></i>
                </button>
            </div>
        </div>

        <div v-for="member in members">
            <!-- Отображение участников -->
            <div v-if="member.id != memberToEdit.id" class="members-item">
                <span>{{ member.name }}</span>
                <span>{{ member.role }}</span> 
                <span>{{ member.group.name }}</span>
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

<style lang="scss" scoped>
    .members-item{
        padding: 0.5rem;
        margin: 0.5rem 0;
        border: 1px solid silver;
        box-shadow: 0 0 4px silver;
        display: flex;
        justify-content: space-between;
    }
</style>
