<template>
  <div
    class="start-screen h-screen flex flex-col justify-center items-center text-blue-100">
    <img
      src="/images/reelPolytechnicLogo.png"
      alt="Reel Polytechnic Logo"
      class="max-w-72 mb-4" />
    <h2 class="text-3xl text-blue-50 uppercase font-bold mb-2">
      Phishing Awareness Trainer
    </h2>

    <div
      v-if="isLoading"
      class="loading-container w-full max-w-md px-4 text-center">
      <p class="text-2xl mb-4">Loading...</p>
      <div class="flex justify-center items-center">
        <div
          class="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-400"></div>
      </div>
    </div>

    <div v-else class="start-game w-full max-w-md px-4">
      <AuthState v-slot="{ loggedIn, user, clear }">
        <div v-if="loggedIn" class="text-center">
          <p class="text-xl mb-2">Welcome, {{ user.email }}!</p>

          <p class="mb-4" v-if="user.bestScore > 0">
            Your best score: {{ bestScorePercentage }}%
          </p>

          <button
            @click="
              async () => {
                await startGame();
              }
            "
            class="bg-blue-200 text-zinc-800 rounded-full px-12 py-3 text-lg font-semibold hover:bg-blue-300 transition-colors mb-4">
            Start Game
          </button>

          <button
            @click="logout"
            class="block text-center mx-auto uppercase text-blue-300 underline text-sm font-semibold transition-colors mb-2">
            Logout
          </button>
        </div>

        <div v-else>
          <h2 class="text-2xl mb-4 text-center">Enter Your Email to Play</h2>
          <p class="text-sm mb-4 text-center">
            New to Reel Polytechnic? We'll create an account for you!
          </p>
          <form
            @submit.prevent="requestLogin"
            class="flex flex-col items-center">
            <input
              v-model="email"
              type="email"
              placeholder="Your Email Address"
              required
              class="w-full px-4 py-2 mb-4 text-black rounded" />
            <button
              type="submit"
              class="bg-white text-zinc-800 rounded-full px-6 py-3 text-lg font-semibold hover:bg-gray-200 transition-colors">
              Send Login Link
            </button>
          </form>
        </div>
      </AuthState>
    </div>

    <div v-if="loginMessage" class="mt-4 text-center text-green-400">
      {{ loginMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useGameState } from "@/composables/gameState";
import { useUserSession } from "#imports";

const { initializeGame, gameStarted, loadingProgress } = useGameState();
const { clear, fetch: fetchSession } = useUserSession();
const isLoading = ref(true);
const email = ref("");
const loginMessage = ref("");

const startGame = () => {
  gameStarted.value = true;
};

const requestLogin = async () => {
  try {
    await $fetch("/api/auth/login-request", {
      method: "POST",
      body: { email: email.value },
    });
    loginMessage.value =
      "Login link sent to your email. If this is your first time, we've created an account for you. Please check your inbox.";
    email.value = "";
  } catch (error) {
    console.error("Login request failed:", error);
    loginMessage.value = "Failed to send login link. Please try again.";
  }
};

const logout = async () => {
  try {
    await $fetch("/api/auth/logout", { method: "POST" });
    await clear();
    loginMessage.value = "Logged out successfully.";
  } catch (error) {
    console.error("Logout failed:", error);
  }
};

// Load scenarios on mount and handle loading state
onMounted(async () => {
  await initializeGame();
  await fetchSession();
  setTimeout(() => {
    isLoading.value = false;
  }, 500); // A small delay to ensure smoother transition after loading
});

// Computed property for bestScore percentage
const bestScorePercentage = computed(() => {
  const user = useUserSession().user;
  return user.value.bestScore > 0 ? (user.value.bestScore / 5) * 100 : 0;
});
</script>
