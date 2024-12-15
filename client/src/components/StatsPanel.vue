<script setup>
    import { useId, computed } from 'vue';

    const unique_ud = useId()
    const collapse_id = computed(() => { return `collapseStats_${unique_ud}` }) 

</script>

<template>
     <div class="stats-panel">
            <a class="text-reset text-decoration-none" :href="'#'+collapse_id" data-bs-toggle="collapse" role="button" aria-expanded="false" :aria-controls="collapse_id">
                <h4 class="text-center">Статистика</h4>
            </a>            
            <div class="collapse" :id="collapse_id">
                <div class="d-flex row justify-content-center m-2">
                    <slot></slot>
                </div>
            </div>
        </div>
</template>