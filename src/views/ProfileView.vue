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
    <div v-if="user" class="container">
        <div class="profile">
            <div class="profile-header card-header shadow">
                <img :src="'../../uploads/' + user.profile_photo" alt="Profile Picture" class="profile-pic shadow">
                <div class="about">
                    <h3>{{ user.firstname }} {{ user.lastname }}</h3>
                    <p>{{ user.location }}</p>
                    <p>Member since {{ formatDate(user.joined_on) }}</p>
                    <p class="bio">{{ user.biography }}</p>
                </div>
                <div class="logistics">
                    <div class="likes-follows">
                        <div :class="{ 'item': true, 'align': isOwnProfile }">
                            <!-- adjust to similar logic like the follow -->
                            <p class="number">{{ postCount }}</p>
                            <p class="title">Posts</p>
                        </div>
                        <div :class="{ 'item': true, 'align': isOwnProfile }">
                            <p class="number">{{ followersCount }}</p>
                            <p class="title">Followers</p>
                        </div>
                    </div>
                    <button v-if="!isOwnProfile" class="btn" :class="{'follow-btn': isFollowed, 'bg-primary': !isFollowed}" :disabled="isFollowed" @click="follow">{{ followText }}</button>
                </div>
            </div>
            <div class="profile-posts">
                <div v-for="post in posts" :key="post.id">
                    <div class="post-media">
                        <img :src="'../../uploads/' + post.photo" alt="Post Picture" class="post-pic">
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div v-else>Loading user...</div>
</template>

<style scoped>
.container{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-bottom: 100px;
}

.profile-header {
    display: flex;
}

.profile .profile-pic {
    width: 200px;
    height: 200px;
    border-radius: 10%;
    margin-right: 10px;
}

.profile .card-header {
    width: 1200px;
    height: auto;
    padding: 20px;
    display: flex;
    flex-direction: row;
    align-items: center;
    background-color: white;
}

.profile .about {
    padding: 25px;
    border-radius: 5px;
    margin-bottom: 20px;
}

.profile .about h3 {
    font-weight: bold;
    margin-bottom: 18px;
}

.profile .about p {
    margin-bottom: 5px;
}

.profile .about .bio {
    margin-top: 18px;
    margin-right: 0px;
}

.profile .logistics {
    display: flex;
    flex-direction: column;
    align-items: end;
    margin-left: auto;
    padding-right: 50px;
}

.profile .likes-follows {
    display: flex;
    justify-content: space-around; 
    width: 100%; 
    margin-bottom: 60px;
    font-size: 18px;
    font-weight: bold;
}

.profile .number {
    font-size: 22px;
    font-weight: bold;
}

.item {
    text-align: center; 
}

.align {
    padding-left: 50px;
}

.profile .item p {
    margin: 0;
}

.profile .item .title {
    color: rgb(160, 160, 160);
}

.follow-btn {
    background-color: green;
    color: rgb(255, 255, 255);
}

/* ----Post Section ---- */
.profile-posts {
    margin-top: 50px;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); /* 3 columns, minimum width of 300px */
    gap: 20px; /* Gap between grid items */
}

.profile-posts .post-media {
    width: 100%;
    height: 350px;
    overflow: hidden; 
}

.profile-posts .post-pic {
    width: 500px;
    height: 100%;
    object-fit: cover; /* Maintain aspect ratio */
}
</style>