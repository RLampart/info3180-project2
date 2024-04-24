<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand label" href="/"><i class="bi bi-camera icon"></i> Photogram</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <RouterLink class="nav-link active" to="/">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link active" to="/explore">Explore</RouterLink>
            </li>
            <li class="nav-item" v-if="loggedIn">
              <RouterLink class="nav-link active" :to="`/users/${userId}`"  @click="reloadIfOnUserProfile">My Profile</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink v-if="!loggedIn" class="nav-link active" to="/login">Login</RouterLink>
              <RouterLink v-if="loggedIn" class="nav-link active" @click="logout" to="/logout">Logout</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div v-if = "feedback" :class="category">
      <ul>
        <li v-for="message in messages">{{ message }}</li>
      </ul>   
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink, useRoute, useRouter } from 'vue-router';
import { userId, loggedIn } from '../views/user';

const router = useRouter();
const route = useRoute();
let csrf_token = ref("");

var feedback = ref(false);
let messages = ref([]);
let category = ref("alert alert-danger");

function getCsrfToken() {
fetch('/api/v1/csrf-token').then((response) => response.json())
  .then((data) => {
    csrf_token.value = data.csrf_token;
  })
};

function reloadIfOnUserProfile() {
  // Check if the current route is a user profile
  if (route.path.startsWith(`/users/`)) {
    setTimeout(() => {
      window.location.reload(); // Reload the page
    }, 1); 
  }
}

const logout = () => {
  const token = localStorage.getItem('token');
  fetch("/api/v1/auth/logout", {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'X-CSRFToken': csrf_token.value,
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    localStorage.clear();
    console.log('Token Removed From Localstorage');
    loggedIn.value = false;

    category = "alert alert-success";
    messages = [data["message"]];

    setTimeout(() => {
      feedback.value = false;
      router.push('/');
    }, 1000);

    feedback.value = true; 
  });
};

const checkLogin = () => {
  const token = localStorage.getItem('token');
  loggedIn.value = token !== null; // Update loggedIn based on the presence of token
};

onMounted(() => {
  checkLogin(); // Check login status when the component is mounted
  getCsrfToken();
  document.addEventListener('logout', logout);
}); 
</script>

<style>
.label {
  font-family: 'Brush Script MT', cursive;
  font-size: 20px
}

.icon {
  color: black;
  padding-right: 5px;
}

ul, ol {
  list-style-type: none;
  padding-left: 0; /* Optional: Remove default padding */
}
</style>