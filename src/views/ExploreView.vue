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

const getCsrfToken = () => {
    fetch('/api/v1/csrf-token')
    .then(data => {
        console.log(data);
        csrf_token.value = data.csrf_token;
    });
};

const makePost = async () => {
    router.push(`/api/v1/users/${userId}/posts`)
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
        })
        .then(response => response.json())
        .then((data) => {
            // posts.value = data.data;

            // Test post results
            posts.value = [
                {
                    id: 1,
                    user: {
                        user_id: 1,
                        profile_photo: 'test.jpg',
                        username: 'qxeenolight'
                    },
                    photo: 'test.jpg',
                    caption: 'This is a post caption',
                    likes: 10,
                    created_on: '2024-04-19'
                },
                {
                    id: 2,
                    user: {
                        user_id: 2,
                        profile_photo: 'cat.jpg',
                        username: 'kxngodarkness'
                    },
                    photo: 'himiko_toga.jpg',
                    caption: 'This is a post caption',
                    likes: 10,
                    created_on: '2024-04-19'
                },
            ];
            console.log("Post Fetched")
        })
    } catch (error) {
        console.log(error)
    }
};

onMounted(() => {
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
    <div v-if = "feedback" :class="category">
        <ul>
            <li v-for="message in messages">{{ message }}</li>
        </ul>   
    </div>

    <div class="container">
        <div class="explore">
            <Post :post="post" v-for="post in posts" :key="post.id" />
        </div>

        <!-- Add New Post -->
        <div class="btn new-post-btn bg-primary" @click="makePost">New Post</div>
    </div>
</template>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 25px;
}

.explore {
    width: 100%;
    max-width: 800px;
    height: 80vh;
}

.new-post-btn {
    position: absolute;
    top: 140px;
    right: 80px;
    background-color: #007bff;
    color: #fff;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
}
</style>