<template>
  <form @submit.prevent="requestLogin">
    <input
      v-model="email"
      type="email"
      placeholder="Your Email Address"
      required />
    <button type="submit">Send Login Link</button>
  </form>
</template>

<script setup>
import { ref } from "vue";

const email = ref("");

async function requestLogin() {
  try {
    await $fetch("/api/auth/login-request", {
      method: "POST",
      body: { email: email.value },
    });
    // Show success message to user
  } catch (error) {
    console.error("Login request failed:", error);
    // Show error message to user
  }
}
</script>
