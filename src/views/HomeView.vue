<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { loggedIn } from '../views/user';

const router = useRouter();
let message = ref("Share photos of your favourite moments with friends, family and the world.")

function goToRegister() {
  router.push({ path: '/register' });
}

function goToLogin() {
  router.push({ path: '/login' });
}

const emitLogout = () => {
  const event = new Event('logout');
  document.dispatchEvent(event);
  router.push('/');
};

onMounted(() => {
  applyFlexStyles();
});

function applyFlexStyles() {
  const container = document.querySelector('.container');
  if (container) {
    container.style.display = 'flex';
    container.style.flexDirection = 'row';
  }
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
          <button v-if="!loggedIn" type="button" class="btn bg-primary" @click="goToLogin">Login</button>
          <button v-if="loggedIn" type="button" class="btn bg-primary" @click="emitLogout">Logout</button>

        </div>
      </div>
    </div>
</template>

<style scoped>
.container {
  justify-content: center;
  align-items: left;
  height: 80vh;
  padding-top: 50px;
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

.text-container h1 {
  font-family: 'Brush Script MT', cursive;
  font-weight: bold;
  font-size: 60px;
}

.icon2 {
  font-size: 40px;
}

.cshadow {
  box-shadow: 0 0 1px rgba(0, 0, 0, 0.1), 0 0 5px rgba(0, 0, 0, 0.438);
}
</style>