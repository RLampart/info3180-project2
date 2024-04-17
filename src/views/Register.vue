<template>
    <div v-if = "feedback" :class="category">
    <ol>
      <li v-for="message in messages">{{ message }}</li>
    </ol>
     
  </div>

  <div class = container>
      <form id='userForm' @submit.prevent="saveUser" method="post" enctype="multipart/form-data">
      <div class="form-group col-md-3">
      <label for="username" class="form-label">Username</label>
      <input type="text" id="username" class="form-control" />
      </div>
      <div class="form-group col-md-3">
      <label for="password" class="form-label">Password</label>
      <input type = "password" id="password" class="form-control" />
      </div>  
      <div class="form-group col-md-3">
      <label for="fname" class="form-label">First Name</label>
      <input type = "text" id="fname" class="form-control" />
      </div>  
      <div class="form-group col-md-3">
      <label for="lname" class="form-label">Last Name</label>
      <input type = "text" id="lname" class="form-control"/>
      </div>  
      <div class="form-group col-md-3">
      <label for="email" class="form-label">Email</label>
      <input type = "email" id="email" class="form-control"/>
      </div>  
      <div class="form-group col-md-3">
      <label for="location" class="form-label">Location</label>
      <input type = "text" id="location" class="form-control"/>
      </div>  
      <div class="form-group col-md-3">
      <label for="bio" class="form-label">Biography</label>
      <textarea id="bio" class="form-control"/>
      </div>  
     <div class="form-group col-md-3">
      <label for="photo" class="form-label">Profile Photo</label>
      <input type="file" id="photo" class="form-control" />
     </div>
    <button type="submit" name="submit" class="btn btn-success">Register</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted  } from "vue";
let csrf_token = ref("");
var feedback = ref(false);
let messages = "";
let category = ref("alert alert-danger");
function getCsrfToken() {
fetch('/api/v1/csrf-token').then((response) => response.json())
.then((data) => {
    console.log(data);
    csrf_token.value = data.csrf_token;
 })
 } ;
onMounted(() => {
getCsrfToken();
}); 
function saveUser(){
  feedback.value = false;
  let userForm = document.getElementById('userForm');
  let form_data = new FormData(userForm);
  fetch("/api/v1/register", {
    method: 'POST',
    body: form_data,
    headers: {'X-CSRFToken': csrf_token.value }
  }).then(function (response) {
     return response.json();
   }).then(function (data) {
// display a success message
    console.log(data);
    userForm.reset();
    if (data['message'] != undefined){
       category = "alert alert-success";
       messages = [data["message"]];
    }else{
      category = "alert alert-danger";
       messages = data;
    }feedback.value = true; 

   }).catch(function (error) {
     console.log(error);
     userForm.reset();
     category = "alert alert-danger";
     messages = error;
     feedback.value = true;  
   });
   }
  
</script>

<style>
/* Add any component specific styles here */
.form-group{
  padding-bottom: 10px;
}
</style>