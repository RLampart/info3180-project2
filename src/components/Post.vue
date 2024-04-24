<script setup>
import { useRouter } from 'vue-router';

const props = defineProps(['post']);
const router = useRouter();

// Function to navigate to the user's profile page
const goToUserProfile = (userId) => {
    // Move to user profile
    router.push(`/users/${userId}`)
};

// Function to format the date
const formatDate = (dateString) => {
    const date = new Date(dateString);
    const options = {day: '2-digit', month: 'short', year: 'numeric'};
    return date.toLocaleDateString('en-UK', options);
};

</script>

<template>
    <div class="card col col-md-4">
        <div class="card-header">
            <img :src="'../../uploads/' + post.user.profile_photo" alt="Profile Picture" class="profile-pic"> 
            <a href="#" @click="goToUserProfile(post.user.user_id)"><strong>{{ post.user.username }}</strong></a>
        </div>
        <div class="post-media">
            <img :src="'../../uploads/' + post.photo" alt="Post Picture" class="post-pic">
        </div>
        <div class="post-details">
            <p>{{ post.caption }}</p>
            <div class="post-footer">

            <!-- Implements Like Logic to appear hollow until clicked -->
            <!-- <p><i class="bi bi-heart"></i> {{ post.likes }} Likes</p> -->
            <p>
                <i class="bi bi-heart" @click="likePost" :class="{ 'bi-heart-fill': post.liked }"></i>
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
    /* border: 1px solid #ccc; */
    margin-bottom: 50px;
    height: auto;
    width: 650px;
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
    height: 400px;
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