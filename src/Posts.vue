<script setup>
import { ref, onMounted  } from "vue";
import { useRouter } from 'vue-router';
import { userId } from './user';

const router = useRouter();
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

function newPost(){
    feedback.value = false;
    const token = localStorage.getItem('token');
    let postForm = document.getElementById('postForm');
    let formdata = new FormData(postForm);

    fetch(`/api/v1/users/${userId['_value']}/posts`, {
        method: 'POST',
        body: formdata,
        headers: { 
            'X-CSRFToken': csrf_token.value,
            'Authorization': `Bearer ${token}`,
        }
    })
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        // display a success message
        console.log(data);
        postForm.reset();

        category = "alert alert-success";
        messages =  [data["message"]];
        feedback.value = true; 
        setTimeout(() => {
            feedback.value = false;
            router.push('/posts/new');
        }, 2000);

    }).catch(function (error) {
        messages = error;
        postForm.reset();
        category = "alert alert-danger";
        messages = error;
        feedback.value = true;  
    });
}

onMounted(() => {
    getCsrfToken();
}); 
</script>

<template>
    <div v-if = "feedback" :class="category">
        <ol>
            <li v-for="message in messages">{{ message }}</li>
        </ol>   
    </div>

    <div class = 'newPost-container container'>
        <h4>New Post</h4>
        <form class='postform shadow' id='postForm' @submit.prevent="newPost" method="POST">
            <div class="form-group col-md-12">
                <label for="photo" class="form-label">Photo</label>
                <input type="file" name="photo" id="photo" class="form-control" />
            </div>
            <div class="form-group col-md-12 caption">
                <label for="caption" class="form-label">Caption</label>
                <textarea name="caption" id="caption" class="form-control" placeholder="Write a caption..."></textarea>
            </div>  

            <button type="submit" name="submit" class="btn btn-success">Submit</button>
        </form>
    </div>
</template>

<style scoped>
.newPost-container {
    width: 30%;
}

h4 {
    padding-bottom: 10px;
}

.postform {
    flex-direction: column;
    height: auto;
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

.form-label{
    font-weight: bold;
}

.caption {
    padding-top: 20px;
}

button.btn{
    margin: 0 auto;
    margin-top: 5%;
    display: block;
    width:100%;
    border: none;
    background-color: #70bb1f;
}
</style>