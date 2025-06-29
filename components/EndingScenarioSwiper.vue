<template>
  <div class="flex flex-col h-dvh justify-between">
    <TransitionCard
      v-if="isTransitionCardVisible"
      :game-stage="'ending'"
      :is-last-regular-scenario="true"
      @proceed="handleMoveToNextStage" />
    <!-- Floating Text Container -->
    <div
      class="flex-none h-1/6 flex items-center justify-center pointer-events-none px-6">
      <p class="text-xl text-white leading-snug text-center">
        {{ currentCard?.text }}
      </p>
    </div>

    <!-- Slides/Cards Container -->
    <div class="absolute h-screen w-screen flex items-center justify-center">
      <swiper-container
        ref="swiperRef"
        :modules="modules"
        effect="tinder"
        :slides-per-view="1"
        :allow-touch-move="true"
        observer
        observer-parents
        :init="false"
        class="w-full h-full">
        <swiper-slide
          v-for="(card, index) in endingScenario.cards"
          :key="index"
          class="h-full flex flex-col items-center justify-center">
          <div class="relative w-full h-4/6 flex items-center justify-center">
            <div
              class="w-[calc(100vh*13/19*0.6)] max-w-[90vw] h-full rounded-xl overflow-hidden transition-transform duration-600 absolute">
              <div class="w-full h-full">
                <div
                  class="absolute inset-0 bg-cover bg-center rounded-xl border-8 border-white"
                  :style="{ backgroundImage: `url(${card.image})` }">
                  <!-- Card content here -->
                </div>
              </div>
            </div>
          </div>
        </swiper-slide>
      </swiper-container>
    </div>
    <DebugPanel
      :current-scenario="endingScenario"
      :current-card-index="currentCardIndex"
      :current-card="currentCard"
      :game-stage="'ending'"
      :score="playerState.score"
      @complete-scenario="handleCompleteScenario"
      @move-to-next-stage="handleMoveToNextStage"
      @skip-to-game-over="setGameOver" />

    <!-- Controls Container -->
    <div class="flex-none h-1/6 flex flex-col justify-end pb-safe">
      <div class="flex justify-center gap-5 z-10 py-2 mb-4">
        <button
          @click="handlePreviousClick"
          :disabled="!canNavigateBack"
          class="flex items-center justify-center shadow-md cursor-pointer transition-transform duration-200 hover:scale-110"
          style="
            width: var(--swiper-tinder-button-size);
            height: var(--swiper-tinder-button-size);
          ">
          <BackButton />
        </button>
        <button
          @click="handleNextClick"
          :disabled="!canNavigate"
          class="flex items-center justify-center shadow-md cursor-pointer transition-transform duration-200 hover:scale-110"
          style="
            width: var(--swiper-tinder-button-size);
            height: var(--swiper-tinder-button-size);
          ">
          <NextButton />
        </button>
      </div>
    </div>
    <div
      v-if="currentCardIndex === endingScenario.cards.length - 1"
      class="fixed bottom-20 left-0 right-0 flex justify-center">
      <button
        @click="moveToNextStage"
        class="bg-blue-500 text-white px-4 py-2 rounded">
        See Final Results
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { register } from "swiper/element/bundle";
import EffectTinder from "~/effect-tinder.esm";
import { useGameState } from "@/composables/gameState";
import BackButton from "./BackButton.vue";
import NextButton from "./NextButton.vue";

register();

const modules = [EffectTinder];
const swiperRef = ref(null);
const currentCardIndex = ref(0);

const {
  playerState,
  moveToNextStage,
  completeCurrentScenario,
  gameSequence,
  setGameOver,
} = useGameState();

// This should be replaced with actual ending scenarios based on score ranges
const endingScenarios = [
  {
    minScore: 0,
    maxScore: 5,
    scenario: {
      /* Low score ending */
    },
  },
  {
    minScore: 6,
    maxScore: 10,
    scenario: {
      /* Medium score ending */
    },
  },
  {
    minScore: 11,
    maxScore: 15,
    scenario: {
      /* High score ending */
    },
  },
  // Add more scenarios as needed
];
const handleCompleteScenario = async () => {
  await completeCurrentScenario();
  isTransitionCardVisible.value = true;
};

const handleMoveToNextStage = () => {
  isTransitionCardVisible.value = false;
  moveToNextStage();
};

const endingScenario = computed(() => {
  const score = playerState.value.score;
  return endingScenarios.find(
    (scenario) => score >= scenario.minScore && score <= scenario.maxScore
  ).scenario;
});

const currentCard = computed(() => {
  return endingScenario.value.cards[currentCardIndex.value];
});

const canNavigate = computed(
  () => currentCardIndex.value < endingScenario.value.cards.length - 1
);
const canNavigateBack = computed(() => currentCardIndex.value > 0);

const handleNextClick = () => {
  if (canNavigate.value && swiperRef.value) {
    swiperRef.value.swiper.slideNext();
    currentCardIndex.value++;
  } else {
    moveToNextStage(); // Move to game over when reaching the end of the ending scenario
  }
};

const handlePreviousClick = () => {
  if (canNavigateBack.value && swiperRef.value) {
    swiperRef.value.swiper.slidePrev();
    currentCardIndex.value--;
  }
};

onMounted(() => {
  if (swiperRef.value) {
    const swiperParams = {
      modules: [EffectTinder],
      effect: "tinder",
      slidesPerView: 1,
      allowTouchMove: true,
    };
    Object.assign(swiperRef.value, swiperParams);
    swiperRef.value.initialize();
  }
});
</script>
