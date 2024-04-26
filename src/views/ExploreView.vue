<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from 'vue-router';
import Post from "@/components/Post.vue";

let csrf_token = ref("");
const router = useRouter();
const posts = ref([]);

var feedback = ref(false);
let messages = ref([]);
let category = ref("alert alert-danger");

const checklogin = () =>{
    if (localStorage.getItem('token') == undefined){
        router.push('/')
    }
}

const getCsrfToken = () => {
    fetch('/api/v1/csrf-token')
    .then(data => {
        csrf_token.value = data.csrf_token;
    });
};

const makePost = async () => {
    router.push('/posts/new');
}

const fetchPosts = async () => {
    // Fetch posts from the database
    console.log("Fetching posts..");

    try {
        const token = localStorage.getItem('token');
        const response = await fetch("/api/v1/posts", {
            method: 'GET',
            headers: { 
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json' 
            }
        });
        const data = await response.json();
        posts.value = data.posts;
        console.log("Post Fetched")
    } catch (error) {
        console.error("Error fetching posts:", error);
    }
};

onMounted(() => {
    checklogin();
    fetchPosts();
    getCsrfToken();
    applyFlexStyles();
});

function applyFlexStyles() {
    const container = document.querySelector('.container');
    if (container) {
        container.style.display = 'flex';
        container.style.flexDirection = 'column';
        container.style.alignItems = 'center';
    }
};
</script>

<template>
    <div class="container">
        <p>{{ message }}</p>
    </div>
</template>

<style>

</style>