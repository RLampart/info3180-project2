<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from 'vue-router';
import { userId } from '../views/user';

const csrf_token = ref('');

const props = defineProps(['post']);
const post = ref(props.post);
const router = useRouter();
const isLiked = ref(false);

const getCsrfToken = () => {
    fetch('/api/v1/csrf-token')
    .then(data => {
        csrf_token.value = data.csrf_token;
    });
};

// Function to navigate to the user's profile page
const goToUserProfile = (userId) => {
    // Move to user profile
    router.push(`/users/${userId}`)
};

const getUserDetail = (userId) => {
    const username = ref('');
    const profile_photo = ref('');

    const fetchUser = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`/api/v1/users/${userId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (!response.ok) {
                throw new Error(`Failed to fetch user: ${response.status}`);
            }
            const data = await response.json();
            username.value = data.username;
            profile_photo.value = data.profile_photo;
        } catch (error) {
            console.error("Error fetching user:", error);
        }
    };

    fetchUser(); // Fetch the username when the component is created
    return { username, profile_photo };
};

const userDetail = getUserDetail(post.value.user_id);

const likePost = async () => {
    const token = localStorage.getItem('token');

    try {
        const response = await fetch(`/api/v1/posts/${post.value.id}/like`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ current_user_id: userId })
        });

        if (!response.ok) {
            throw new Error('Failed to like post');
        }

        post.value.likes++;
        isLiked.value = true;
        
    } catch (error) {
        console.error('Error liking post:', error);
    }
} 

const checkIfLiked = async () => {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/v1/posts/${post.value.id}/is_liking`, {
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
            if (data.is_liking) {
                isLiked.value = true;
            } 
        } else {
            throw new Error('Failed to check if liked:', response.statusText);
        }
    } catch (error) {
        console.error('An error occurred:', error);
    }
};

// Function to format the date
const formatDate = (dateString) => {
    const date = new Date(dateString);
    const options = {day: '2-digit', month: 'short', year: 'numeric'};
    return date.toLocaleDateString('en-UK', options);
};

// Computed property to format the username and profile photo
const formattedUserDetail = computed(() => {
    return {
        username: userDetail.username.value.replace(/\"/g, ''),
        profile_photo: userDetail.profile_photo.value.replace(/\"/g, '')
    };
});

onMounted(() => {
    getCsrfToken();
    checkIfLiked();
});
</script>

<template>
    <div class="card col col-md-4">
        <div class="card-header">
            <img :src="'../../uploads/' + formattedUserDetail.profile_photo" alt="Profile Picture" class="profile-pic"> 
            <a @click="goToUserProfile(post.user_id)"><strong>{{ formattedUserDetail.username }}</strong></a>
        </div>
        <div class="post-media">
            <img :src="'../../uploads/' + post.photo" alt="Post Picture" class="post-pic">
        </div>
        <div class="post-details">
            <p>{{ post.caption }}</p>
            <div class="post-footer">
            <p>
                <i class="bi" @click="likePost" :class="{'bi-heart-fill': isLiked, 'bi-heart': !isLiked, 'disabled-icon': isLiked}" :style="{ pointerEvents: isLiked ? 'none' : 'auto' }"></i>
                {{ post.likes }} Likes
            </p>

            <p><strong>{{ formatDate(post.created_on) }}</strong></p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.card {
    display: flex;
    margin-bottom: 50px;
    height: auto;
    width: 640px;
}

.card-header {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
    background-color: white;
}

.card-header a {
    text-decoration: none; 
    color: inherit; 
    cursor: pointer;
}

.profile-pic {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    margin-right: 10px;
}

.post-details {
    flex: 1;
    padding-top: 20px;
    padding-left: 15px;
    padding-right: 15px;
}

.post-pic {
    width: 100%;
    height: 450px;
}

.post-footer {
    display: flex;
    justify-content: space-between;
}

/* Likes Logic */
.bi-heart {
    cursor: pointer;
}

.bi-heart-fill {
    color: red;
}
</style>