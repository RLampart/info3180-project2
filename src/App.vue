<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
</script>

<template>
  <AppHeader />

  <main>
    <RouterView />
  </main>
  
  <AppFooter />
</template>

<style>
body {
  padding-top: 90px;
  background-color: #F5EFE6;
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
</style>