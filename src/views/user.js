// Store of some sort

import { ref } from 'vue';

const userId = ref(localStorage.getItem('userId'));
const loggedIn = ref('');

const updateUserId = (newId) => {
    userId.value = newId;
    localStorage.setItem('userId', newId);
};

const checkLogin = () => {
    const token = localStorage.getItem('token');
    loggedIn.value = token !== null; // Return the login status based on the presence of the token
};

export { userId, updateUserId, loggedIn, checkLogin };