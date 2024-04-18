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
              <RouterLink to="/" class="nav-link active">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link active" to="/explore">Explore</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link active" to="/">My Profile</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link active" to="/logout">Logout</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router";
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
</style>