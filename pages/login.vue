<template>
  <div
    class="start-screen h-screen flex flex-col justify-center items-center text-gray-100">
    <img
      src="/images/reelPolytechnicLogo.png"
      alt="Reel Polytechnic Logo"
      class="max-w-72 mb-8" />

    <div class="w-full max-w-md px-4 text-center">
      <h2 class="text-2xl mb-2 text-center font-display mt-12">Login Error</h2>
      <p class="text-xl mb-4">{{ errorMessage }}</p>
      <button
        class="bg-blue-500 text-white rounded-full px-6 py-3 text-lg font-semibold hover:bg-blue-600 transition-colors"
        @click="goToHome">
        Go back to login
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const errorMessage = ref("");

const errorMessages: Record<string, string> = {
  missing_token: "Login token is missing. Please try again.",
  invalid_token: "Invalid login token. Please request a new login link.",
  user_not_found: "User not found. Please check your email or sign up.",
  default: "An error occurred. Please try again.",
};

onMounted(() => {
  const error = route.query.error as string;
  if (error) {
    errorMessage.value = errorMessages[error] || errorMessages.default;
  }
});

const goToHome = () => {
  router.push("/");
};
</script>

<style scoped>
.start-screen {
  background-image: url("/images/home-bg.png");
  background-size: cover;
  background-position: center;
}
</style>
