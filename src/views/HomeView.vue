<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
let message = ref("Share photos of your favourite moments with friends, family and the world.")

function goToRegister() {
  router.push({ path: '/register' });
}

function goToLogin() {
  router.push({ path: '/login' });
}
</script>

<template>
    <div class="container">
      <div class="image-container cshadow">
        <img alt="Splash Image" class="image" src="@/assets/landing_photo.jpg"/>
      </div>
      <div class="text-container cshadow">
        <h1 class="text-center"><i class="bi bi-camera icon2"></i> Photogram</h1>
        <hr>
        <p>{{ message }}</p>
        <div class="button">
          <button type="button" class="btn bg-success" @click="goToRegister">Register</button>
          <button type="button" class="btn bg-primary" @click="goToLogin">Login</button>
        </div>
      </div>
    </div>
</template>

<style>
body {
  background-color: #F5EFE6;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 90vh;
}

.image-container,
.text-container,
.image {
  height: 450px;
  width: 650px;
  background-color: white;
  border-radius: 5px;
}

.image-container {
  margin-right: 15px;
}

.text-container {
  padding: 50px;
  font-size: 22px;
}

/* @import url('https://fonts.googleapis.com/css2?family=Dancing+Script&display=swap'); */

.text-container h1 {
  font-family: 'Brush Script MT', cursive;
  font-weight: bold;
  font-size: 60px;
}

.icon2 {
  font-size: 40px;
}

.button {
  padding-top: 50px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn {
  width: 250px;
  height: 45px;
  color: white;
  font-size: 18px;
}

.btn:hover {
  color: white;
}

.btn:not(:disabled):not(.disabled):active,
.btn:not(:disabled):not(.disabled).active {
  color: white !important;
}

.cshadow {
  box-shadow: 0 0 1px rgba(0, 0, 0, 0.1), 0 0 5px rgba(0, 0, 0, 0.438);
}
</style>