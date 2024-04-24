<script setup>
import { ref, onMounted  } from "vue";
import { useRouter } from 'vue-router';
import { updateUserId, loggedIn } from './user';

let csrf_token = ref("");
var feedback = ref(false);
const router = useRouter()
let messages = ref([]);
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
function login(){
  feedback.value = false;
  let userForm = document.getElementById('loginForm');
  let formdata = new FormData(userForm);
  var object = {};
formdata.forEach(function(value, key){
    object[key] = value;
});
var json = JSON.stringify(object);
  fetch("/api/v1/auth/login", {
    method: 'POST',
    body: json,
    headers: {'X-CSRFToken': csrf_token.value,
             'Content-Type':'application/json' }
  }).then(function (response) {
     return response.json();
   }).then(function (data) {
// display a success message
    console.log(data);
    userForm.reset();
    if (data['token'] != undefined){
       category = "alert alert-success";
       messages = [data["message"]];
       localStorage.setItem("token",data['token']);
       loggedIn.value = true;
       updateUserId(data.id);

      // Delay Switching Route to Display message
      setTimeout(() => {
        router.push('/explore');
      }, 500);
       //redirect
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

<template>
    <div v-if = "feedback" :class="category">
    <ol>
      <li v-for="message in messages">{{ message }}</li>
    </ol>   
   </div>

  <div class = 'login-container container'>
    <h4>Login</h4>
      <form class='shadow' id='loginForm' @submit.prevent="login" method="post">
      <div class="form-group col-md-12">
      <label for="username" class="form-label">Username</label>
      <input type="text" name="username" id="username" class="form-control" />
      </div>
      <div class="form-group col-md-12">
      <label for="password" class="form-label">Password</label>
      <input type = "password" name="password" id="password" class="form-control" />
      </div>  

    <button type="submit" name="submit" class="btn btn-success">Login</button>
    </form>
  </div>
</template>

<style scoped>
.login-container{
  flex-direction: column;
  height: auto;
  width: 30%;
}

h4 {
  padding-bottom: 10px;
}

form{
  background-color: white;
  padding: 30px;
  
}
.form-group{
  padding: 10px;
}
.form-control{
  align-self: center;
  justify-self: center;
}

.login-container > #password{
  margin-bottom: 10%;
}
.form-label{
  font-weight: bold;
}

button.btn{
  margin: 0 auto;
  margin-top: 15%;
  display: block;
  width:100%;
  border: none;
  background-color: #70bb1f;
}
</style>