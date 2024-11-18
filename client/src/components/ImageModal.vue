<script setup>
    import { ref } from 'vue';
    import { Modal } from 'bootstrap/dist/js/bootstrap'

    const props = defineProps({ 
        title: String, 
        image: String 
    })

    const modalRef = ref()

    function show() {
        const modal = new Modal(modalRef.value)
        modal.show()
    }

    // Функции, которые можно вызывать из вне
    defineExpose({
        show
     })

</script>

<template>
    <div class="modal fade" id="imageModal" tabindex="-1" aria-labelledby="imageModalLabel" aria-hidden="true" ref="modalRef">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="imageModalLabel">{{ props.title }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body" style="width: auto">
                    <img :src="props.image">
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
img{
    object-fit: cover;
    width: 100%;
}
</style>