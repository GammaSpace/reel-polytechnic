<template>
  <div
    class="game-over-screen flex flex-col items-center justify-center text-white">
    <!-- <img :src="gameOverArt" alt="Game Over Art" class="mb-4" /> -->
    <img
      src="/images/reelPolytechnicLogo.png"
      alt="Reel Polytechnic Logo"
      class="max-w-72 mb-4" />
    <div class="end-game w-full max-w-md px-4">
      <h1 class="text-3xl font-bold mb-2 font-display mt-8">
        {{ gameOverTitle }}
      </h1>

      <p class="text-lg mb-4 font-body" v-html="gameOverText" />

      <div
        class="flex flex-row justify-between w-full mb-12 border-t-2 border-t-zinc-600 border-b-2 border-b-zinc-600 py-2">
        <p class="uppercase text-md text-gray-300">
          Your Score:
          <span class="text-white font-bold">{{ finalScorePercentage }}%</span>
        </p>
        <p class="uppercase text-md text-gray-300">
          Best Score:
          <span class="text-white font-bold">{{ bestScorePercentage }}%</span>
        </p>
      </div>

      <p v-if="isNewBestScore" class="text-lg font-bold text-yellow-400 mb-6">
        New Best Score!
      </p>
      <button
        class="bg-blue-500 px-6 py-2 rounded-full hover:bg-blue-600"
        @click="restartGame">
        Play Again
      </button>
    </div>
  </div>
</template>

<script>
import { useUserSession } from "#imports";
import confetti from "canvas-confetti";

export default {
  props: {
    finalScore: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      isNewBestScore: false,
    };
  },
  computed: {
    bestScorePercentage() {
      const user = useUserSession().user;
      const bestScore = user.value.bestScore || 0;
      return bestScore > 0 ? (bestScore / 5) * 100 : 0;
    },
    finalScorePercentage() {
      return (this.finalScore / 5) * 100;
    },
    gameOverTitle() {
      if (this.isNewBestScore) {
        return "New Personal Best!";
      } else if (this.finalScore === 5) {
        return "Congratulations!";
      } else if (this.finalScore >= 4) {
        return "Wow, Great Job!";
      } else {
        return "Better Luck Next Time!";
      }
    },
    gameOverText() {
      if (this.finalScore === 5) {
        return "Perfect score! You've aced every challenge and proven your phishing detection skills are top-notch. You've now been entered in the grand prize draw for a new monitor!<br><br>Stay vigilant!";
      } else if (this.finalScore >= 4) {
        return "You did great! You've achieved an impressive score! You've now been entered into the prize draw for a new webcam!<br><br>Keep honing those skills and stay vigilant!";
      } else {
        return "You're almost there! You've completed the game, but didn't hit the mark. Give it another shot! A higher score means a chance at the prize draw from a webcam or the grand prize draw for a monitor!<br><br>Remember, practice makes perfect and every attempt strengthens your defenses!";
      }
    },
  },
  mounted() {
    this.updateScore();
  },
  methods: {
    async updateScore() {
      try {
        const response = await fetch("/api/update-score", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ score: this.finalScore }),
        });

        if (!response.ok) {
          throw new Error("Failed to update score");
        }

        const result = await response.json();
        console.log("Score updated:", result);

        const user = useUserSession().user;
        user.value.bestScore = result.bestScore;

        this.isNewBestScore = result.isNewBestScore;

        this.checkAndTriggerConfetti();
      } catch (error) {
        console.error("Error updating score:", error);
      }
    },
    restartGame() {
      this.$emit("restart-game");
    },
    triggerConfetti() {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { x: 0.5, y: 0.5 },
      });
    },
    checkAndTriggerConfetti() {
      if (this.isNewBestScore || this.finalScore > 3) {
        this.triggerConfetti();
      }
    },
  },
};
</script>

<style scoped>
.game-over-screen {
  background-image: url("/images/home-bg.png");
  height: 100vh;
  padding: 20px;
  text-align: center;
}
</style>
