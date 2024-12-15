<script setup>
    import { onBeforeMount } from 'vue';
    import axios from 'axios';
    import Cookies from 'js-cookie';
    import { storeToRefs } from 'pinia';
    import { useUserStore } from '@/stores/userStore';

    const userStore = useUserStore()
    const userInfo = storeToRefs(userStore)

    onBeforeMount(() => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    })

</script>

<template>
    <a v-if="userInfo.isSuperuser.value" type="button" class="btn btn-success" href="/api/export/xlsx/">Export in xlsx</a>
</template>