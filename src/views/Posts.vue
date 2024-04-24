<script setup>
import { ref } from "vue";

let message = ref("Posts View")
// /api/v1/users/<int:user_id>/posts


</script>

<template>
    <div class="container">
        <h3>Register</h3>
        <form id='userForm' @submit.prevent="saveUser" method="post" enctype="multipart/form-data">
            <div class="form-group col-md-10">
                <label for="username" class="form-label">Username</label>
                <input type="text" name="username" id="username" class="form-control" />
            </div>
            <div class="form-group col-md-10">
                <label for="password" class="form-label">Password</label>
                <input type = "password" name="password" id="password" class="form-control" />
            </div>  
            <div class="form-group col-md-10">
                <label for="first_name" class="form-label">First Name</label>
                <input type = "text" name="first_name" id="first_name" class="form-control" />
            </div>  
            <div class="form-group col-md-10">
                <label for="last_name" class="form-label">Last Name</label>
                <input type = "text" name="last_name" id="last_name" class="form-control"/>
            </div>  
            <div class="form-group col-md-10">
                <label for="email" class="form-label">Email</label>
                <input type = "email" name="email" id="email" class="form-control"/>
            </div>  
            <div class="form-group col-md-10">
                <label for="location" class="form-label">Location</label>
                <input type = "text" name="location" id="location" class="form-control"/>
            </div>  
            <div class="form-group col-md-10">
                <label for="bio" class="form-label">Biography</label>
                <textarea name="bio" id="bio" class="form-control"></textarea>
            </div>  
            <div class="form-group col-md-10">
                <label for="photo" class="form-label">Profile Photo</label>
                <input type="file" name="photo" id="photo" class="form-control" />
            </div>
            <button type="submit" name="submit" class="btn btn-success">Register</button>
        </form>
    </div>
</template>

<style>

</style>