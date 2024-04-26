<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from 'vue-router';
import { userId } from '../views/user';

const csrf_token = ref('');

const router = useRouter();
const user = ref();
const posts = ref([]);

const followersCount = ref(0); // Initialize with 0
const isFollowed = ref(false);
const followText = ref('Follow');
const postCount = ref(0);

const isOwnProfile = ref(false);

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

// Fetch Followers Count
const fetchFollowers = async () => {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/v1/users/${router.currentRoute.value.params.id}/follow`, {
        method: 'GET',
        headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json' 
        }
    });
    const data = await response.json();
    followersCount.value = data.follower_count;
    } catch (error) {
        console.error('Error fetching followers count:', error);
    }
};

const follow = () => {
    const token = localStorage.getItem('token');
    fetch(`/api/users/${router.currentRoute.value.params.id}/follow`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token.value,
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify({ current_user_id: userId })
    })
    .then(response => {
        if (response.ok) {
            fetchFollowers();
            isFollowed.value = true;
            followText.value = 'Following';
            return response.json();
        } else {
            throw new Error('Failed to follow user:', response.statusText);
        }
    })
    .then(data => {
        console.log(data.message); // Log the success message
    })
    .catch(error => {
        console.error('An error occurred:', error);
    });
};

const checkIfFollowing = async () => {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/v1/users/${router.currentRoute.value.params.id}/is_following`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token.value,
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify({ current_user_id: userId })
        });
        if (response.ok) {
            const data = await response.json();
            if (data.is_following) {
                isFollowed.value = true;
                followText.value = 'Following';
            }
        } else {
            throw new Error('Failed to check if following:', response.statusText);
        }
    } catch (error) {
        console.error('An error occurred:', error);
    }
};

const checkOwnership = () => {
    isOwnProfile.value = userId.value == router.currentRoute.value.params.id;
};

const fetchPosts = async () => {
    // Fetch posts from the database
    console.log("Fetching posts..");

    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/v1/users/${router.currentRoute.value.params.id}/posts`, {
            method: 'GET',
            headers: { 
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json' 
            }
        });
        const data = await response.json();
        posts.value = data.posts;
        postCount.value = data.posts.length;
        console.log("Post Fetched")
    } catch (error) {
        console.error("Error fetching posts:", error);
    }
};

const fetchUser = async () => {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/v1/users/${router.currentRoute.value.params.id}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (!response.ok) {
            throw new Error(`Failed to fetch user: ${response.status}`);
        }
        const data = await response.json();
        user.value = data;
    } catch (error) {
        console.error("Error fetching user:", error);
    }
};

// Function to format the date
const formatDate = (dateString) => {
    const date = new Date(dateString);
    // Format the date into "Month Year" format
    const formattedDate = new Intl.DateTimeFormat('en-US', { month: 'long', year: 'numeric' }).format(date);
    return formattedDate
};

onMounted(() => {
    checklogin();
    getCsrfToken();
    checkOwnership();
    checkIfFollowing();
    fetchFollowers();
    fetchUser();
    fetchPosts();
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