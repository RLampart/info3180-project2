<script setup>
import { ref, onMounted  } from "vue";
import {useRouter } from 'vue-router';
let message = ref("Logout View");

const router = useRouter()
onMounted(() => {
localStorage.removeItem('token');
router.push('/');
}); 
</script>

<template>
    <div class="container">
        <p>{{ message }}</p>
    </div>
</template>

<style>

</style>