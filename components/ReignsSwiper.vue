<template>
  <Transition name="game-fade" mode="out-in">
    <StartGameScreen v-if="!gameStarted" key="start-screen" />
    <EndingScenarioSwiper v-else-if="isPlayingEndingScenario" key="ending" />
    <GameOverScreen
      v-else-if="gameOver"
      key="game-over"
      :finalScore="playerState.score"
      @restart-game="resetGame" />
    <div v-else key="main-game" class="relative">
      <TransitionCard
        v-if="isTransitionCardVisible"
        :title="getTransitionCardTitle"
        :message="getTransitionCardMessage"
        :button-text="getTransitionCardButtonText"
        @proceed="handleMoveToNextStage" />

      <div
        v-if="currentScenario && currentCard"
        class="flex flex-col h-dvh justify-between">
        <!-- Floating Text Container -->
        <div
          class="flex-none h-1/6 flex items-center justify-center pointer-events-none p-6">
          <Transition name="fade" mode="out-in">
            <div
              v-if="currentCard && currentCard.text"
              :key="currentCardIndex"
              class="card-text text-sm text-white leading-snug text-center"
              v-html="parseCardText(currentCard.text)"></div>
            <div
              v-else-if="lastDecisionText"
              :key="'last-decision'"
              class="card-text text-sm text-white leading-snug text-center"
              v-html="parseCardText(lastDecisionText)"></div>
            <div
              v-else
              key="no-text"
              class="text-sm text-white leading-snug text-center">
              <!-- You can add a loading message or leave it empty -->
            </div>
          </Transition>
        </div>

        <!-- Slides/Cards Container -->
        <div
          class="flex-grow absolute h-full w-full flex items-center justify-center overflow-hidden">
          <!-- Scenario Transition Loading -->
          <div
            v-if="isScenarioTransitioning"
            class="scenario-loading flex flex-col items-center justify-center text-white z-50 transition-opacity duration-300">
            <p class="text-xl font-medium opacity-90 animate-pulse mb-6">
              Loading next scenario...
            </p>
            <div class="flex space-x-2">
              <div
                class="w-3 h-3 bg-white rounded-full opacity-90 drop-shadow-lg"
                style="
                  animation: smoothBounce 1.4s infinite ease-in-out;
                  animation-delay: 0ms;
                "></div>
              <div
                class="w-3 h-3 bg-white rounded-full opacity-90 drop-shadow-lg"
                style="
                  animation: smoothBounce 1.4s infinite ease-in-out;
                  animation-delay: 150ms;
                "></div>
              <div
                class="w-3 h-3 bg-white rounded-full opacity-90 drop-shadow-lg"
                style="
                  animation: smoothBounce 1.4s infinite ease-in-out;
                  animation-delay: 300ms;
                "></div>
            </div>
          </div>

          <swiper-container
            v-if="isDataReady && !isScenarioTransitioning"
            ref="swiperRef"
            :modules="modules"
            effect="tinder"
            :slides-per-view="1"
            :allow-touch-move="true"
            observer
            observer-parents
            :init="false"
            class="w-full h-full transition-opacity duration-300 scenario-entrance">
            <swiper-slide
              v-for="(card, index) in filteredCards"
              :key="index"
              class="flex items-center justify-center">
              <div
                :ref="
                  (el) => {
                    if (el) cardRefs[index] = el;
                  }
                "
                class="card-container relative"
                :class="{ 'is-flipped': isRevealCardFlipped }">
                <div
                  :class="[
                    'card-face front absolute inset-0 rounded-xl overflow-hidden transition-transform duration-600',
                    { 'rotate-y-180': cardFlipStates[card.id] },
                  ]">
                  <div
                    class="absolute inset-0 bg-cover bg-center rounded-xl border-8 border-white aspect-[11/19]"
                    :style="{
                      backgroundImage: `url(${getCardImage(card, true)})`,
                    }">
                    <Transition name="pop-fade">
                      <div
                        v-if="
                          card.type === 'decision' &&
                          showDecisionIcon &&
                          !isCardSwiping
                        ">
                        <button
                          @click.stop="toggleOverlay(card)"
                          class="focus:outline-none absolute top-4 right-4 bg-yellow-200 text-black leading-none rounded-full p-2 shadow-lg icon-pop z-30">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="32"
                            height="32"
                            viewBox="0 0 256 256">
                            <path
                              fill="currentColor"
                              d="M196 96c0 29.47-24.21 54.05-56 59.06v.94a12 12 0 0 1-24 0v-12a12 12 0 0 1 12-12c24.26 0 44-16.15 44-36s-19.74-36-44-36s-44 16.15-44 36a12 12 0 0 1-24 0c0-33.08 30.5-60 68-60s68 26.92 68 60m-68 92a20 20 0 1 0 20 20a20 20 0 0 0-20-20" />
                          </svg>
                        </button>
                      </div>
                    </Transition>
                    <!-- Overlay -->
                    <Transition :name="overlayTransitionName">
                      <div
                        v-if="card.showOverlay"
                        class="absolute inset-0 bg-zinc-800 bg-opacity-90 flex flex-col text-gray-200 p-4 z-50">
                        <div>
                          <button
                            @click.stop="toggleOverlay(card)"
                            class="focus:outline-none absolute top-4 right-4 bg-yellow-200 text-black leading-none rounded-full p-2 shadow-lg icon-pop z-30">
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              width="32"
                              height="32"
                              fill="none"
                              viewBox="0 0 24 24"
                              stroke="currentColor">
                              <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M6 18L18 6M6 6l12 12" />
                            </svg>
                          </button>
                        </div>
                        <div class="flex-grow overflow-y-auto overlay">
                          <div
                            v-if="card.loadedOverlayContent"
                            v-html="card.loadedOverlayContent"
                            class="overlay-content"></div>
                          <p v-else>Loading content...</p>
                        </div>
                      </div>
                    </Transition>

                    <!-- Enhanced full-height trust/distrust labels -->
                    <div
                      class="absolute inset-0 w-full h-full flex items-center justify-center text-center z-20 transition-all duration-300 swiper-tinder-label swiper-tinder-label-no pointer-events-none transform scale-105"
                      data-swiper-parallax="-300"
                      data-swiper-parallax-duration="600"
                      style="
                        background: linear-gradient(
                          135deg,
                          rgba(239, 68, 68, 0.9),
                          rgba(185, 28, 28, 0.9)
                        );
                        backdrop-filter: blur(2px);
                      ">
                      <div
                        class="flex flex-col items-center space-y-2 md:space-y-4">
                        <div
                          class="text-5xl md:text-6xl lg:text-7xl font-black uppercase tracking-wider drop-shadow-2xl animate-bounce-slow">
                          👎
                        </div>
                        <div
                          class="text-2xl md:text-3xl lg:text-4xl font-black uppercase tracking-wider drop-shadow-2xl text-white"
                          style="text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8)"
                          v-html="card.distrustLabel || 'DISTRUST'"></div>
                        <div
                          class="w-20 h-1 bg-white rounded-full opacity-75 shadow-lg"></div>
                      </div>
                    </div>
                    <div
                      class="absolute inset-0 w-full h-full flex items-center justify-center text-center z-20 transition-all duration-300 swiper-tinder-label swiper-tinder-label-yes pointer-events-none transform scale-105"
                      data-swiper-parallax="-300"
                      data-swiper-parallax-duration="600"
                      style="
                        background: linear-gradient(
                          135deg,
                          rgba(34, 197, 94, 0.9),
                          rgba(21, 128, 61, 0.9)
                        );
                        backdrop-filter: blur(2px);
                      ">
                      <div
                        class="flex flex-col items-center space-y-2 md:space-y-4">
                        <div
                          class="text-5xl md:text-6xl lg:text-7xl font-black uppercase tracking-wider drop-shadow-2xl animate-bounce-slow">
                          👍
                        </div>
                        <div
                          class="text-2xl md:text-3xl lg:text-4xl font-black uppercase tracking-wider drop-shadow-2xl text-white"
                          style="text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8)"
                          v-html="card.trustLabel || 'TRUST'"></div>
                        <div
                          class="w-20 h-1 bg-white rounded-full opacity-75 shadow-lg"></div>
                      </div>
                    </div>
                  </div>
                </div>
                <!-- Back face (reveal card) -->
                <div
                  v-if="card.type === 'reveal'"
                  :class="[
                    'card-face back absolute inset-0 rounded-xl overflow-hidden transition-transform duration-600 border-8 border-white',
                    {
                      'rotate-y-180': !cardFlipStates[card.id],
                      'mfa-reveal-card': currentScenario.scenarioType === 'mfa',
                      'regular-reveal-card':
                        currentScenario.scenarioType !== 'mfa',
                    },
                  ]"
                  :style="{
                    backgroundImage: `url(${getCardImage(card, false)})`,
                  }"
                  class="w-full h-full">
                  <!-- MFA-specific reveal card content -->
                  <template v-if="currentScenario.scenarioType === 'mfa'">
                    <div class="h-full absolute inset-0 bg-cover bg-center">
                      <div
                        class="h-full absolute inset-0 bg-opacity-90 flex flex-col overflow-y-auto justify-between bg-stone-200">
                        <div class="flex flex-col h-full justify-between">
                          <!-- Sash container -->
                          <div class="top-0 left-0 w-full">
                            <!-- Sash -->
                            <div
                              :class="[
                                'w-full text-center font-display py-4 text-white text-2xl font-bold uppercase',
                                card.isCorrect ? 'bg-green-500' : 'bg-red-500',
                              ]">
                              {{ card.isCorrect ? "Correct!" : "Incorrect!" }}
                            </div>
                          </div>
                          <div class="flex flex-col justify-between">
                            <div class="pt-6 px-3">
                              <p
                                class="font-display font-black text-black mb-2 text-center text-xl">
                                {{ card.userAction }}
                              </p>
                            </div>
                            <div class="p-3">
                              <p
                                class="text-center text-lg text-white mb-1 flex flex-col items-center justify-center">
                                <span
                                  class="text-base leading-tight rounded-md text-black">
                                  <div>{{ card.outcome }}</div>
                                </span>
                              </p>
                            </div>
                          </div>
                          <div
                            class="learning-objective text-stone-800 p-3 self-end">
                            <p
                              class="font-display text-base md:text-lg pb-20 text-stone-800 text-center leading-snug">
                              {{ currentScenario.learningObjectives }}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </template>

                  <template v-else>
                    <div
                      class="regular-reveal-content h-full flex flex-col justify-start items-center">
                      <div
                        class="w-full h-full p-4 text-white bg-gradient-to-b from-blue-600 to-transparent">
                        <p
                          v-if="card.feedback"
                          class="text-2xl text-center font-display embossed-text text-blue-100"
                          v-html="parseCardText(card.feedback)" />
                        <p v-else class="text-xl px-8">No feedback available</p>
                      </div>
                    </div>
                  </template>
                </div>
                <div
                  v-if="isTransitionCard"
                  class="absolute inset-0 bg-gray-800 bg-opacity-90 flex flex-col items-center justify-center text-white p-4 z-50">
                  <h2 class="text-2xl font-bold mb-4">Scenario Complete</h2>
                  <p class="mb-6 text-center">
                    You've completed this scenario. Ready to move to the next
                    one?
                  </p>
                  <button
                    @click="moveToNextScenario"
                    class="bg-blue-500 text-white px-6 py-3 rounded-full text-lg font-semibold hover:bg-blue-600 transition-colors">
                    Proceed to Next Scenario
                  </button>
                </div>
              </div>
            </swiper-slide>
          </swiper-container>
          <div
            v-else-if="!isScenarioTransitioning"
            class="h-full flex flex-col items-center justify-center text-white scenario-loading">
            <p class="text-xl font-medium opacity-90 animate-pulse mb-6">
              Loading scenarios...
            </p>
            <div class="flex space-x-2">
              <div
                class="w-3 h-3 bg-white rounded-full opacity-90 drop-shadow-lg"
                style="
                  animation: smoothBounce 1.4s infinite ease-in-out;
                  animation-delay: 0ms;
                "></div>
              <div
                class="w-3 h-3 bg-white rounded-full opacity-90 drop-shadow-lg"
                style="
                  animation: smoothBounce 1.4s infinite ease-in-out;
                  animation-delay: 150ms;
                "></div>
              <div
                class="w-3 h-3 bg-white rounded-full opacity-90 drop-shadow-lg"
                style="
                  animation: smoothBounce 1.4s infinite ease-in-out;
                  animation-delay: 300ms;
                "></div>
            </div>
          </div>
        </div>

        <!-- Controls Container -->
        <div
          class="h-1/6 flex flex-col align-middle items-center justify-start w-full"
          :class="{
            'pointer-events-none opacity-50': isScenarioTransitioning,
          }">
          <div class="px-6 w-full flex flex-col items-center space-y-4 z-10">
            <div
              class="flex justify-center gap-5 z-10 py-2 mb-4 space-x-4 w-full">
              <a
                href="/"
                @click.prevent="returnToStartScreen"
                class="p-2 self-center">
                <HomeButton />
              </a>
              <button
                @click="
                  isDecisionCard ? handleDistrustClick() : handlePreviousClick()
                "
                :disabled="(!canNavigateBack && !isDecisionCard) || isFlipping"
                :class="[
                  '-mt-12 flex items-center justify-center cursor-pointer transition-transform duration-200 hover:scale-110',
                  {
                    'opacity-50 cursor-not-allowed':
                      (!canNavigateBack && !isDecisionCard) || isFlipping,
                  },
                ]">
                <BackButton v-if="!isDecisionCard" />
                <div
                  v-else-if="currentScenario?.scenarioType === 'mfa'"
                  class="bg-red-400 rounded-full py-2 px-4 font-bold text-base">
                  DENY
                </div>
                <ThumbsDown v-else />
              </button>

              <button
                @click="isDecisionCard ? handleTrustClick() : handleNextClick()"
                :disabled="!canNavigateForward || isFlipping"
                :class="[
                  '-mt-12 flex items-center justify-center cursor-pointer transition-transform duration-200 hover:scale-110',
                  {
                    'opacity-50 cursor-not-allowed':
                      !canNavigateForward || isFlipping,
                  },
                ]">
                <NextButton v-if="!isDecisionCard" />
                <span
                  v-else-if="currentScenario?.scenarioType === 'mfa'"
                  class="bg-green-400 rounded-full py-2 px-4 font-bold text-base"
                  >APPROVE</span
                >
                <ThumbsUp v-else />
              </button>

              <button
                @click="retryScenario"
                :disabled="isRetryDisabled"
                class="p-2 bg-transparent border-none"
                :class="{ 'opacity-50': isRetryDisabled }"
                :style="{
                  cursor: isRetryDisabled ? 'not-allowed' : 'pointer',
                }">
                <RetryButton />
              </button>
            </div>
          </div>
        </div>

        <!-- Debug Panel and Button -->
        <DebugPanel
          v-if="!isScenarioTransitioning"
          :current-scenario="currentScenario"
          :current-scenario-index="currentScenarioIndex"
          :current-card-index="currentCardIndex"
          :current-card="currentCard"
          :game-sequence="gameSequence"
          :game-stage="gameStage"
          :is-ready-for-ending="isReadyForEnding"
          :score="playerState.score"
          :regular-scenarios-count="regularScenarios.length"
          @jump-to-scenario="handleJumpToScenario"
          @complete-scenario="handleCompleteScenario"
          @skip-to-decision="handleSkipToDecision"
          @skip-to-ending="skipToEndingScenario"
          @move-to-next-stage="handleMoveToNextStage"
          @skip-to-game-over="skipToGameOver" />
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, computed } from "vue";
import { register } from "swiper/element/bundle";
import EffectTinder from "~/effect-tinder.esm";
import { useGameState } from "@/composables/gameState";
import "/assets/css/styles.css";
import { useMarkdownContent } from "~/composables/useMarkdownContent";

register();
const showDebugPanel = ref(false);

const toggleDebugPanel = () => {
  showDebugPanel.value = !showDebugPanel.value;
};

const modules = [EffectTinder];
const swiperRef = ref(null);
const swiper = ref(null);
const cardRefs = ref([]);
const isTransitioning = ref(false);
const isScenarioTransitioning = ref(false);
const flipTimeout = ref(null);
const lastDecisionText = ref("");
const isDecisionCard = computed(() => {
  return currentCard.value?.type === "decision";
});
const currentScore = computed(() => playerState.value.score);

const isRevealCardFlipped = ref(false);

const parseCardText = (text) => {
  if (!text) return ""; // Return an empty string if text is undefined or null
  console.log("Parsing card text:", text);
  return text.replace(/\n/g, "<br>");
};
const isFlipping = ref(false);

const selectedScenarioId = ref(null);

const {
  cardFlipStates,
  completeCurrentScenario,
  currentCard,
  currentCardIndex,
  currentScenario,
  currentScenarioIndex,
  filteredCards,
  gameOver,
  gameSequence,
  gameStage,
  gameStarted,
  initializeGame,
  isEndingScenario,
  isLastCardOfScenario,
  isLastRegularScenario,
  jumpToScenario,
  jumpToScenarioById,
  makeChoice,
  moveToNextScenario,
  moveToNextStage,
  nextCard,
  nextScenario,

  playerState,
  previousCard,
  resetCardFlipStates,
  resetGame,
  setGameOver,
  scenarios,
  userChoices,
  isTransitionCardVisible,
} = useGameState();

const isTransitionCard = computed(() => {
  return currentCard.value && currentCard.value.type === "transition";
});
const isReadyForEnding = computed(() => {
  if (!currentScenario.value || !currentScenario.value.cards) {
    // Handle the scenario where currentScenario or its cards are not yet defined
    console.log("Current scenario or its cards are undefined.");
    return false;
  }

  return (
    currentScenarioIndex.value === gameSequence.value.length - 1 &&
    currentCardIndex.value === currentScenario.value.cards.length - 1
  );
});

const handleCompleteScenario = async () => {
  console.log("handleCompleteScenario called");
  await completeCurrentScenario();
};

const handleMoveToNextStage = () => {
  console.log("handleMoveToNextStage called");
  moveToNextStage();
};

const getTransitionCardTitle = computed(() => {
  if (isLastRegularScenario.value) return "Main Scenarios Complete";
  if (isEndingScenario.value) return "Ending Scenario Complete";
  return "Scenario Complete";
});

const getTransitionCardMessage = computed(() => {
  if (isLastRegularScenario.value)
    return "You've completed all main scenarios. Ready to see your ending?";
  if (isEndingScenario.value)
    return "You've completed the ending scenario. Ready to review your choices?";
  return "You've completed this scenario. Ready to move to the next one?";
});

const getTransitionCardButtonText = computed(() => {
  if (isLastRegularScenario.value) return "Proceed to Ending";
  if (isEndingScenario.value) return "Proceed to Recap";
  return "Next Scenario";
});

const regularScenarios = computed(() =>
  scenarios.value.filter(
    (s) =>
      s.scenarioType !== "ending" &&
      (s.cards.find((card) => card.type === "decision")?.trustChoice
        ?.consequences?.length > 0 ||
        s.cards.find((card) => card.type === "decision")?.distrustChoice
          ?.consequences?.length > 0)
  )
);

const endingScenarios = computed(() =>
  scenarios.value.filter((s) => s.scenarioType === "ending")
);

const unplayedRegularScenarios = computed(() => {
  return regularScenarios.value.filter(
    (scenario) => !userChoices.value[scenario.id]
  );
});

const skipToEndingScenario = () => {
  moveToNextStage();
};

// Smooth scenario transition with elegant fade animations
const smoothScenarioTransition = async () => {
  console.log("Starting smooth scenario transition");
  isTransitioning.value = true;

  // Step 1: Wait for swipe animation to complete, then fade out cards
  setTimeout(async () => {
    console.log("Step 1: Fading out current cards");
    const swiperEl = document.querySelector("swiper-container");
    if (swiperEl) {
      swiperEl.style.transition = "opacity 0.4s ease-out";
      swiperEl.style.opacity = "0";
    }

    // Step 2: After cards fade out, show loading screen
    setTimeout(async () => {
      console.log("Step 2: Showing loading screen");
      isScenarioTransitioning.value = true;

      // Step 3: Wait for loading to be visible, then change scenario
      setTimeout(async () => {
        console.log("Step 3: Changing scenario");
        // Reset state and move to next scenario
        isRevealCardFlipped.value = false;
        decisionFeedback.value = "";
        lastDecisionText.value = "";

        await moveToNextScenario();
        currentCardIndex.value = 0;

        // Wait for scenario change to register
        await nextTick();

        // Step 4: Fade out loading screen and prepare for cards
        setTimeout(async () => {
          console.log("Step 4: Hiding loading and preparing new cards");
          const loadingEl = document.querySelector(".scenario-loading");
          if (loadingEl) {
            loadingEl.style.transition = "opacity 0.3s ease-out";
            loadingEl.style.opacity = "0";
          }

          // Step 5: After loading fades out, show new cards with fade in
          setTimeout(() => {
            console.log("Step 5: Showing new cards");
            isScenarioTransitioning.value = false;

            // Wait for new swiper to be created, then fade it in
            nextTick(() => {
              const newSwiperEl = document.querySelector("swiper-container");
              if (newSwiperEl) {
                newSwiperEl.style.opacity = "0";
                newSwiperEl.style.transition = "opacity 0.5s ease-in";

                // Trigger fade in
                setTimeout(() => {
                  newSwiperEl.style.opacity = "1";

                  // Clean up transitions after animation
                  setTimeout(() => {
                    newSwiperEl.style.transition = "";
                    isTransitioning.value = false;
                    console.log("Scenario transition complete with fade-in");
                  }, 500);
                }, 50);
              } else {
                isTransitioning.value = false;
              }
            });
          }, 300); // Wait for loading fade out
        }, 600); // Show loading for a moment
      }, 200); // Brief moment for loading to appear
    }, 400); // Wait for cards to fade out
  }, 300); // Wait for swipe to complete
};

// Update transitionToNextScenario
const transitionToNextScenario = async () => {
  isTransitioning.value = true;
  isRevealCardFlipped.value = false; // Reset flip state

  if (currentScenarioIndex.value < regularScenarios.value.length - 1) {
    // Move to the next regular scenario
    currentScenarioIndex.value++;
    currentCardIndex.value = 0;
  } else {
    // We're at the end of the ending scenario, start recap
    moveToNextStage();

    isTransitioning.value = false;
    return;
  }

  currentCardIndex.value = 0;
  isRevealCardFlipped.value = false;
  decisionFeedback.value = "";
  cardFlipStates.value = {};
  lastDecisionText.value = "";

  if (currentScenario.value.cards) {
    currentScenario.value.cards.forEach((card) => {
      if (!card.id) {
        card.id = `card-${Date.now()}-${Math.random()}`;
      }
      cardFlipStates.value[card.id] = false;
      card.showOverlay = false;
      card.overlayContent = null;
    });
  }

  await nextTick();
  if (swiper.value) {
    swiper.value.slideTo(0, 0);
    await swiper.value.update();
  }

  isTransitioning.value = false;
};

const decisionFeedback = ref("");
let swipingTimeout = null;

watch(
  () => currentCard.value,
  (newCard) => {
    console.log("Current card changed:", newCard);
    if (newCard?.type === "reveal") {
      console.log("Reveal card detected, scheduling flip");
      setTimeout(flipRevealCard, 1000);
    } else {
      console.log("Resetting reveal card flip");
      isRevealCardFlipped.value = false;
    }
  }
);

const allScenariosComplete = computed(() => {
  return (
    currentScenarioIndex.value >= scenarios.value.length - 1 &&
    Object.keys(userChoices.value).length === scenarios.value.length
  );
});

const setScore = (score) => {
  playerState.value.score = score;
  // Optionally, adjust other playerState properties here
};

const completeAllScenarios = () => {
  if (scenarios.value.length > 0) {
    currentScenarioIndex.value = scenarios.value.length - 1;
    if (scenarios.value[currentScenarioIndex.value].cards.length > 0) {
      currentCardIndex.value =
        scenarios.value[currentScenarioIndex.value].cards.length - 1;
    } else {
      console.error("No cards found in the final scenario");
    }
  } else {
    console.error("No scenarios available");
  }
};

const isInMainScenarios = computed(
  () =>
    !isEndingScenario.value &&
    currentScenarioIndex.value < scenarios.value.length - 1
);
const isInEndingScenario = computed(() => isEndingScenario.value);

const simulateAllChoices = () => {
  // console.log("Starting simulation of all choices");
  // console.log(`Total regular scenarios: ${regularScenarios.value.length}`);

  regularScenarios.value.forEach((scenario, index) => {
    if (!scenario || scenario.id === null) {
      console.warn(`Invalid scenario found at index ${index}. Skipping.`);
      return;
    }

    // console.log(`Processing scenario ${scenario.id}`);
    const decisionCard = scenario.cards.find(
      (card) => card.type === "decision"
    );
    if (decisionCard) {
      const isTrust = Math.random() < 0.5;
      // console.log(`Scenario ${scenario.id}: Making ${isTrust ? 'trust' : 'distrust'} choice`);
      makeChoice(isTrust, scenario.id);
    } else {
      console.warn(
        `No decision card found for scenario ${scenario.id}. This shouldn't happen based on current data.`
      );
    }
  });

  // console.log("Finished simulating all choices");
  // console.log(`Final score: ${playerState.value.score}`);
};

const skipToGameOver = () => {
  setGameOver(true);
};

const isDataReady = computed(() => {
  const ready =
    !!currentScenario.value &&
    !!currentScenario.value.cards &&
    currentScenario.value.cards.length > 0;
  console.log("isDataReady:", ready);
  console.log("currentScenario:", currentScenario.value);
  return ready;
});

watch(
  () => currentScenario.value,
  (newScenario) => {
    console.log("currentScenario changed:", newScenario);
    if (newScenario && newScenario.cards && newScenario.cards.length > 0) {
      nextTick(() => {
        initializeSwiper();
      });
    }
  },
  { immediate: true }
);
watch(
  () => currentScenario.value,
  async (newScenario) => {
    if (newScenario) {
      currentCardIndex.value = 0;
      await nextTick();
      if (swiper.value) {
        swiper.value.slideTo(0, 0);
        await swiper.value.update();
      }
    }
  },
  { immediate: true }
);

watch(
  () => currentCardIndex.value,
  async (newIndex) => {
    console.log(`Card index changed to ${newIndex}`);
    if (swiper.value) {
      swiper.value.slideTo(newIndex, 0);
    }
  }
);

const scenarioIds = computed(() => {
  return scenarios.value ? scenarios.value.map((scenario) => scenario.id) : [];
});

const canNavigate = computed(() => {
  if (!currentCard.value) return false;
  if (currentCard.value.type === "reveal" && !isRevealCardFlipped.value)
    return false;
  return true;
});

const canNavigateForward = computed(() => {
  if (isDecisionCard.value) return true;
  if (!currentCard.value) return false;
  if (currentCard.value.type === "reveal" && !isRevealCardFlipped.value)
    return false;
  return true;
});

const canNavigateBack = computed(() => {
  if (isDecisionCard.value) return false;
  if (!currentCard.value) return false;
  if (currentCardIndex.value === 0) return false;
  if (currentCard.value.type === "reveal" && isRevealCardFlipped.value)
    return false;
  return true;
});

const handleTinderSwipe = async (s, direction) => {
  if (!isDataReady.value || !currentCard.value) return;

  if (currentCard.value.type === "decision") {
    const isTrust = direction === "right";
    makeChoice(isTrust);
    decisionFeedback.value = isTrust
      ? currentCard.value.trustChoice?.feedback
      : currentCard.value.distrustChoice?.feedback;
    lastDecisionText.value = currentCard.value.text;
    s.slideNext(300, true);
  } else if (currentCard.value.type === "reveal") {
    if (isRevealCardFlipped.value) {
      // Final reveal card swiped - use smooth transition
      await smoothScenarioTransition();
    } else {
      flipRevealCard(currentCardIndex.value);
    }
  }
};

const showDecisionIcon = ref(false);

const handleSlideChangeTransitionEnd = () => {
  if (currentCard.value?.type === "decision") {
    showDecisionIcon.value = false;
    nextTick(() => {
      showDecisionIcon.value = true;
    });
  } else {
    showDecisionIcon.value = false;
  }
};
const isCardSwiping = ref(false);

const handleSlideChange = (s) => {
  if (!isDataReady.value) return;

  currentCardIndex.value = s.activeIndex;
  const card = currentCard.value;

  if (card?.type === "decision") {
    showDecisionIcon.value = false;
    isCardSwiping.value = false;
    nextTick(() => {
      showDecisionIcon.value = true;
    });
  } else if (card?.type === "reveal") {
    if (flipTimeout.value) {
      clearTimeout(flipTimeout.value);
    }
    flipTimeout.value = setTimeout(() => {
      if (!isRevealCardFlipped.value) {
        flipRevealCard(currentCardIndex.value);
      }
    }, 1000);
  } else {
    isRevealCardFlipped.value = false;
    decisionFeedback.value = "";
    showDecisionIcon.value = false;
  }
};

const flipRevealCard = () => {
  if (currentCard.value?.type === "reveal" && !isRevealCardFlipped.value) {
    console.log("Flipping reveal card");
    isRevealCardFlipped.value = true;

    // Add a timeout or use the transitionend event to update the face after the flip is done
    setTimeout(() => {
      // Update the card face here
      currentCard.value = getNextCard();
    }, 600); // Match this time with your CSS transition time
  }
};

// const flipRevealCard = (index) => {
//   console.log("flipRevealCard called for index:", index);
//   const card = currentScenario.value.cards[index];
//   if (card && card.type === 'reveal' && !isRevealCardFlipped.value) {
//     if (flipTimeout.value) {
//       clearTimeout(flipTimeout.value);
//     }
//     isFlipping.value = true;
//     flipTimeout.value = setTimeout(() => {
//       console.log("Flipping card in flipRevealCard");
//       cardFlipStates.value[card.id] = true;
//       isRevealCardFlipped.value = true;
//       isFlipping.value = false;
//     }, 1000);
//   }
// };

const initializeSwiper = async () => {
  console.log("Attempting to initialize swiper...", {
    swiperRef: !!swiperRef.value,
    isDataReady: isDataReady.value,
    gameStarted: gameStarted.value,
    currentScenario: currentScenario.value?.id,
  });

  // Wait a moment for DOM to be ready
  await nextTick();

  if (swiperRef.value && isDataReady.value) {
    try {
      // Reset swiper reference
      swiper.value = null;

      const swiperParams = {
        modules: [EffectTinder],
        effect: "tinder",
        slidesPerView: 1,
        allowTouchMove: true,
        watchSlidesProgress: true,
        virtualTranslate: true,
        on: {
          slideChangeTransitionEnd: handleSlideChangeTransitionEnd,
          progress: function (s, progress) {
            const swiper = this;
            for (let i = 0; i < swiper.slides.length; i++) {
              const slideProgress = swiper.slides[i].progress;
              const absProgress = Math.abs(slideProgress);
              swiper.slides[i].style.opacity = 1 - absProgress / 1;
            }
          },
          setTransition: function (s, duration) {
            const swiper = this;
            for (let i = 0; i < swiper.slides.length; i++) {
              swiper.slides[i].style.transition = `${duration}ms`;
            }
          },
          slideChange: (swiper) => {
            handleSlideChange(swiper);
            // Disable swiping on decision and reveal cards
            if (
              currentCard.value?.type === "decision" ||
              currentCard.value?.type === "reveal"
            ) {
              swiper.allowTouchMove = false;
            } else {
              swiper.allowTouchMove = true;
            }
          },
          tinderSwipe: handleTinderSwipe,
          sliderFirstMove: () => {
            if (currentCard.value?.type === "decision") {
              isCardSwiping.value = true;
              if (swipingTimeout) {
                clearTimeout(swipingTimeout);
              }
            }
          },
          sliderMove: () => {
            if (swipingTimeout) {
              clearTimeout(swipingTimeout);
            }
          },
          touchEnd: () => {
            if (currentCard.value?.type === "decision") {
              if (swipingTimeout) {
                clearTimeout(swipingTimeout);
              }
              swipingTimeout = setTimeout(() => {
                isCardSwiping.value = false;
              }, 300);
            }
          },
        },
      };
      Object.assign(swiperRef.value, swiperParams);
      swiperRef.value.initialize();
      swiper.value = swiperRef.value.swiper;
      console.log(
        "✅ Swiper initialized successfully with scenario:",
        currentScenario.value?.id
      );
    } catch (error) {
      console.error("❌ Error initializing Swiper:", error);
    }
  } else {
    console.log("⚠️  Swiper not initialized: missing requirements", {
      swiperRef: !!swiperRef.value,
      isDataReady: isDataReady.value,
      gameStarted: gameStarted.value,
    });
  }
};

onMounted(async () => {
  if (gameStarted.value) {
    initializeGame();
    // Preload ALL scenarios at once
    await preloadAllScenarios();
    await initializeSwiper();
  }
  if (flipTimeout.value) {
    clearTimeout(flipTimeout.value);
  }
});

watch(isDataReady, async (ready) => {
  if (ready && !isScenarioTransitioning.value) {
    await nextTick(); // Wait for DOM to be ready
    await initializeSwiper();
  }
});

watch(isScenarioTransitioning, async (transitioning) => {
  if (!transitioning && isDataReady.value) {
    // Wait for DOM to update after v-if change
    await nextTick();
    console.log("Reinitializing swiper after scenario transition");
    await initializeSwiper();
  }
});

// Watch for gameStarted to initialize swiper when transitioning from start screen
watch(gameStarted, async (started) => {
  if (started && isDataReady.value) {
    // Wait extra time for transition to complete
    await nextTick();
    setTimeout(async () => {
      console.log("Initializing swiper after game start transition");
      await initializeSwiper();
    }, 700); // Wait for transition to complete (600ms + buffer)
  }
});

watch(
  currentScenario,
  async (newScenario, oldScenario) => {
    if (newScenario && newScenario !== oldScenario) {
      console.log("Current scenario changed to:", newScenario.id);
      console.log("New scenario data:", JSON.stringify(newScenario, null, 2));
      resetCardFlipStates();
      cardFlipStates.value = {};
      newScenario.cards.forEach((card, index) => {
        if (!card.id) {
          card.id = `card-${index}`;
        }
        cardFlipStates.value[card.id] = false;
      });

      await nextTick();
      if (!swiper.value) {
        // Ensure Swiper isn't re-initialized unnecessarily
        initializeSwiper();
      }
    }
  },
  { immediate: true }
);

const isPlayingMainScenarios = computed(
  () => gameStarted && currentScenarioIndex < scenarios.length - 1
);

const isPlayingEndingScenario = computed(
  () =>
    gameStarted && currentScenarioIndex === scenarios.length - 1 && !isRecapMode
);

const swipeRight = async () => {
  if (swiper.value && canNavigate.value && !isTransitioning.value) {
    if (currentCard.value?.type === "reveal" && isRevealCardFlipped.value) {
      // Final reveal card swiped - use smooth transition
      swiper.value.tinder.yes();
      await smoothScenarioTransition();
    } else {
      swiper.value.tinder.yes();
    }
  }
};

const swipeLeft = async () => {
  if (swiper.value && !isTransitioning.value) {
    if (canNavigateBack.value) {
      await previousCard();
      swiper.value.tinder.no();
    } else if (
      currentCard.value?.type === "reveal" &&
      isRevealCardFlipped.value
    ) {
      // Final reveal card swiped - use smooth transition
      swiper.value.tinder.no();
      await smoothScenarioTransition();
    }
  }
};

const returnToStartScreen = () => {
  resetGame();
  gameStarted.value = false;
};

const isRetryDisabled = computed(() => {
  return currentCard.value?.type === "reveal";
});

const retryScenario = async () => {
  if (swiper.value && currentScenario.value && !isRetryDisabled.value) {
    isTransitioning.value = true;

    currentCardIndex.value = 0;

    cardFlipStates.value = {};
    currentScenario.value.cards.forEach((card, index) => {
      if (!card.id) {
        card.id = `card-${index}`;
      }
      cardFlipStates.value[card.id] = false;
      card.showOverlay = false;
      card.overlayContent = null;
    });

    isRevealCardFlipped.value = false;
    decisionFeedback.value = "";
    lastDecisionText.value = "";

    await nextTick();
    if (swiper.value) {
      swiper.value.slideTo(0, 0);
      await swiper.value.update();
    }

    isTransitioning.value = false;
  }
};

const {
  content: markdownContent,
  processInlineMarkdown,
  loadMarkdownFile,
} = useMarkdownContent();
const overlayTransitionName = ref("");

const toggleOverlay = async (card) => {
  console.log("Toggle overlay called for card:", card.id);

  card.showOverlay = !card.showOverlay;

  if (card.showOverlay && card.overlayContent && !card.loadedOverlayContent) {
    try {
      card.loadedOverlayContent = await loadMarkdownFile(card.overlayContent);
    } catch (error) {
      console.error("Error loading markdown:", error);
      card.loadedOverlayContent = "Failed to load content. Please try again.";
    }
  }
};

watch(currentCardIndex, () => {
  overlayTransitionName.value = "";

  // reset the overlay after switching scenarios
  // it is now replaying the same scenario instead of switching to the next one in the sequence
  if (currentCard.value?.showOverlay) {
    currentCard.value.showOverlay = false;
  }
});

watch(
  () => playerState.value,
  (newState, oldState) => {
    // console.log('PlayerState updated:', newState);
    // console.log('Score changed from', oldState.score, 'to', newState.score);
  },
  { deep: true }
);

const renderMarkdown = async (text, isFile = false) => {
  if (!text) return "";
  try {
    if (isFile) {
      return await loadMarkdownFile(text);
    } else {
      return processInlineMarkdown(text);
    }
  } catch (error) {
    console.error("Error rendering markdown:", error);
    return text; // Fallback to plain text if markdown rendering fails
  }
};
const renderedCardText = ref("");
const renderedLastDecisionText = ref("");

watch(
  () => currentCard.value?.text,
  async (newText) => {
    if (newText) {
      renderedCardText.value = await renderMarkdown(newText);
    }
  }
);

watch(
  () => lastDecisionText.value,
  async (newText) => {
    if (newText) {
      renderedLastDecisionText.value = await renderMarkdown(newText);
    }
  }
);

watch(isReadyForEnding, (ready) => {
  console.log("isReadyForEnding changed:", ready);
});

watch(gameStage, (newStage) => {
  console.log("Game stage changed to:", newStage);
});

watch(currentScenarioIndex, (newIndex) => {
  console.log(
    "Current scenario index:",
    newIndex,
    "of",
    gameSequence.value.length
  );
});
watch(currentCardIndex, (newIndex, oldIndex) => {
  console.log(`Card index changed from ${oldIndex} to ${newIndex}`);
  console.log("Current card:", currentCard.value);

  isRevealCardFlipped.value = false; // Reset flip state

  if (currentCard.value?.type === "reveal") {
    setTimeout(() => {
      isRevealCardFlipped.value = true;
    }, 1000);
  }
});

watch(
  cardFlipStates,
  (newStates) => {
    console.log("Updated card flip states:", newStates);
  },
  { deep: true }
);

const getScenarioImage = (scenario) => {
  const decisionCard = scenario.cards.find((card) => card.type === "decision");
  return decisionCard?.image || "/images/card-placeholder.png";
};

const getScoreChange = (scenario) => {
  const choice = userChoices.value[scenario.id];
  return choice ? choice.scoreChange : 0;
};

const handleChoice = async (isTrust) => {
  if (currentCard.value?.type === "decision" && !isFlipping.value) {
    isFlipping.value = true;
    makeChoice(isTrust, currentScenario.value.id);

    const choice = isTrust
      ? currentCard.value.trustChoice
      : currentCard.value.distrustChoice;
    const revealCard = currentScenario.value.cards.find(
      (card) => card.type === "reveal"
    );

    if (revealCard && currentScenario.value.scenarioType === "mfa") {
      revealCard.userAction = isTrust
        ? "You approved the login attempt!"
        : "You denied the login attempt!";
      revealCard.outcome = choice.feedback;
      revealCard.scoreChange = choice.consequences;
      revealCard.isCorrect = choice.consequences === 1;
    } else if (revealCard) {
      revealCard.feedback = choice.feedback;
    }

    // Move to the reveal card
    swiperRef.value.swiper.slideNext();

    // Ensure the reveal card is displayed before flipping
    await nextTick();

    // Flip the reveal card after a short delay
    setTimeout(() => {
      isRevealCardFlipped.value = true;
    }, 1000);

    isFlipping.value = false;
  }
};

const handleJumpToScenario = (scenarioId) => {
  jumpToScenario(scenarioId);
};

const handleSkipToDecision = () => {
  if (!currentScenario.value || !currentScenario.value.cards) return;

  // Find the decision card index
  const decisionCardIndex = currentScenario.value.cards.findIndex(
    (card) => card.type === "decision"
  );

  if (decisionCardIndex !== -1) {
    currentCardIndex.value = decisionCardIndex;
    if (swiper.value) {
      swiper.value.slideTo(decisionCardIndex, 300);
    }
  }
};

const handleTrustClick = () => handleChoice(true);
const handleDistrustClick = () => handleChoice(false);

const handleNextClick = async () => {
  console.log("handleNextClick called");

  // Check if swiper is initialized, if not try to initialize it
  if (!swiper.value) {
    console.log("Swiper not ready, attempting to initialize...");
    await initializeSwiper();
    // If still not ready, use the composable function instead
    if (!swiper.value) {
      console.log("Swiper still not ready, using nextCard function");
      await nextCard();
      return;
    }
  }

  if (!isFlipping.value) {
    if (currentCard.value?.type === "reveal" && isRevealCardFlipped.value) {
      console.log("Final reveal card - starting smooth scenario transition");

      // Make the card swipe away
      if (swiper.value) {
        swiper.value.tinder.yes();
      }

      // Start smooth transition to next scenario
      await smoothScenarioTransition();
    } else if (!isLastCardOfScenario.value) {
      console.log("Moving to next card");
      if (swiper.value) {
        swiper.value.slideNext();
      } else {
        // Fallback to composable function
        await nextCard();
      }
    } else {
      console.log("Last card of scenario, starting smooth transition");

      // For final cards, swipe away and transition
      if (swiper.value) {
        swiper.value.tinder.yes();
      }

      await smoothScenarioTransition();
    }

    // Ensure the swiper slides to the correct index for regular navigation
    await nextTick();
    if (
      swiper.value &&
      currentCard.value?.type !== "reveal" &&
      !isLastCardOfScenario.value
    ) {
      swiper.value.slideTo(currentCardIndex.value, 0);
    }
  }
};

const handlePreviousClick = async () => {
  if (!isFlipping.value && canNavigateBack.value) {
    await previousCard();
    if (swiper.value) {
      swiper.value.slidePrev(300, true);
    }
  }
};

const handleMoveToNextScenario = () => {
  isTransitionCardVisible.value = false;
  moveToNextScenario();
};

const isCorrect = (scenario) => {
  const choice = userChoices.value[scenario.id];
  if (!choice) return false;

  const decisionCard = scenario.cards.find((card) => card.type === "decision");
  if (!decisionCard) return false;

  // For MFA scenarios, we determine correctness based on the consequences value
  if (scenario.scenarioType === "mfa") {
    const chosenConsequences =
      choice.choice === "trust"
        ? decisionCard.trustChoice.consequences
        : decisionCard.distrustChoice.consequences;
    return chosenConsequences === 1;
  }

  // For non-MFA scenarios, we can use the existing logic
  return choice.scoreChange > 0;
};

const preloadedImages = ref(new Set());
const imageLoadingPromises = ref(new Map());

// Add preload function
const preloadImage = (url) => {
  if (!url || preloadedImages.value.has(url)) return Promise.resolve();

  if (imageLoadingPromises.value.has(url)) {
    return imageLoadingPromises.value.get(url);
  }

  const promise = new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => {
      preloadedImages.value.add(url);
      imageLoadingPromises.value.delete(url);
      resolve();
    };
    img.onerror = () => {
      imageLoadingPromises.value.delete(url);
      reject();
    };
    img.src = url;
  });

  imageLoadingPromises.value.set(url, promise);
  return promise;
};

// Preload current and next scenario images
const preloadScenarioImages = async (scenario) => {
  if (!scenario?.cards) return;

  const imagesToPreload = scenario.cards
    .map((card) => {
      if (card.type === "reveal") {
        return [getCardImage(card, true), getCardImage(card, false)];
      }
      return [getCardImage(card, true)];
    })
    .flat();

  await Promise.all(imagesToPreload.map(preloadImage));
};

// Preload next scenarios
const preloadUpcomingScenarios = async () => {
  const currentIndex = currentScenarioIndex.value;
  const scenariosToPreload = gameSequence.value.slice(
    currentIndex,
    currentIndex + 2
  );

  for (const scenarioId of scenariosToPreload) {
    const scenario = scenarios.value.find((s) => s.id === scenarioId);
    if (scenario) {
      await preloadScenarioImages(scenario);
    }
  }
};

// Modify watch handlers
watch(
  currentScenario,
  async (newScenario) => {
    if (newScenario) {
      isScenarioTransitioning.value = true;
      try {
        await preloadScenarioImages(newScenario);
        // Also preload next scenarios in background
        preloadUpcomingScenarios();
      } finally {
        isScenarioTransitioning.value = false;
      }
    }
  },
  { immediate: true }
);

// Modify getCardImage to use cached images
function getCardImage(card, isFront) {
  let imageUrl;
  if (card.type === "reveal" && isFront) {
    imageUrl = "/images/card-back.jpg";
  } else {
    imageUrl = card.image;
  }
  // Trigger preload but don't wait for it
  if (imageUrl) preloadImage(imageUrl);
  return imageUrl;
}

// Add after the existing preload functions
const preloadAllScenarios = async () => {
  console.log("Starting to preload all scenario images...");
  isScenarioTransitioning.value = true;

  try {
    // Preload all scenarios in the game sequence
    for (const scenarioId of gameSequence.value) {
      const scenario = scenarios.value.find((s) => s.id === scenarioId);
      if (scenario) {
        await preloadScenarioImages(scenario);
      }
    }
    console.log("All scenario images preloaded successfully");
  } catch (error) {
    console.error("Error preloading scenario images:", error);
  } finally {
    isScenarioTransitioning.value = false;
  }
};

// Also watch gameStarted to handle when user starts the game
watch(gameStarted, async (started) => {
  if (started) {
    // Preload all scenarios when game starts
    await preloadAllScenarios();
  }
});

// Remove the preloadUpcomingScenarios calls since we're loading everything at once
watch(
  currentScenario,
  async (newScenario) => {
    if (newScenario) {
      // Keep transition state management but don't reload images
      isScenarioTransitioning.value = true;
      try {
        // Images should already be preloaded, just wait a brief moment for transition
        await new Promise((resolve) => setTimeout(resolve, 300));
      } finally {
        isScenarioTransitioning.value = false;
      }
    }
  },
  { immediate: true }
);
</script>

<style>
/* Root variables */
:root {
  --swiper-tinder-no-color: red;
  --swiper-tinder-yes-color: green;
  --swiper-tinder-label-text-color: #fff;
  --swiper-tinder-label-font-size: 32px;
  --swiper-tinder-button-size: 56px;
  --swiper-tinder-button-icon-size: 32px;
  --card-aspect-ratio: 1.2;
  /* Adjust this value to change the card's aspect ratio */
  --card-height: 90%;
  --card-aspect-ratio: 1.2;
  --card-max-height: 70vh;
  --card-horizontal-margin: 5vw;
}

/* 

.card-face.front {
  z-index: 2;
  transform: rotateY(0deg);
}

.card-face.back {
  z-index: 1;
  transform: rotateY(180deg);
}

.card-container.is-flipped .card-face.front {
  z-index: 1;
  transform: rotateY(180deg);
}

.card-container.is-flipped .card-face.back {
  z-index: 2;
  transform: rotateY(0deg);
}


 */

.card-container {
  @apply aspect-[11/19] h-4/6 relative;
  perspective: 2000px;
  transform-style: preserve-3d;
  transition: transform 0.6s;
}

.card-face {
  @apply z-10;
  backface-visibility: hidden;
  position: absolute;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
}

.card-back {
  @apply z-20;
  transform: rotateY(180deg);
  /* Ensure the back starts flipped */
}

.card-face,
.card-back {
  transform-style: preserve-3d;
  width: 100%;
  height: 100%;
  position: absolute;
}

/* Apply backface-visibility only where needed */
.card-face {
  backface-visibility: hidden;
  /* Apply to front face */
}

.card-back {
  backface-visibility: hidden;
  /* Apply to back face */
  transform: rotateY(180deg);
  /* Start flipped */
}

/* Enhance 3D effect for the card container */
.reveal {
  perspective: 2000px;
}

/* Enhance the flip animation */
.transition-transform {
  transition-duration: 0.6s;
  transition-timing-function: ease-out;
}

.rotate-y-180 {
  transform: rotateY(180deg) translate3d(0, 0, 50px);
  z-index: 0;
}

/* Optional: Enhance the reveal card appearance */
.reveal {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

/* Transition styles */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Premium game state transitions */
.game-fade-enter-active,
.game-fade-leave-active {
  transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.game-fade-enter-from {
  opacity: 0;
  transform: scale(0.95) translateY(20px);
  filter: blur(2px);
}

.game-fade-leave-to {
  opacity: 0;
  transform: scale(1.05) translateY(-20px);
  filter: blur(2px);
}

/* Premium scenario transition animations */
.scenario-loading {
  animation: fadeInScale 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes fadeInScale {
  0% {
    opacity: 0;
    transform: scale(0.8) translateY(20px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Enhanced swiper transitions */
swiper-container {
  transition: opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Smooth card entrance */
@keyframes cardFadeIn {
  0% {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.card-container {
  animation: cardFadeIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Initial scenario load animation */
@keyframes scenarioEntrance {
  0% {
    opacity: 0;
    transform: scale(0.9) translateY(30px);
    filter: blur(4px);
  }
  60% {
    opacity: 0.8;
    transform: scale(1.02) translateY(-5px);
    filter: blur(0px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
    filter: blur(0px);
  }
}

.scenario-entrance {
  animation: scenarioEntrance 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Enhanced loading dots */
@keyframes smoothBounce {
  0%,
  20%,
  50%,
  80%,
  100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-8px);
  }
  60% {
    transform: translateY(-4px);
  }
}

/* Swiper specific styles */
.swiper-slide-shadow {
  @apply absolute inset-0 bg-black bg-opacity-15 pointer-events-none z-10;
}

.swiper-slide-active.swiper-slide-swiping .swiper-tinder-label {
  @apply opacity-100;
}

/* Safe area adjustment */
.pb-safe {
  padding-bottom: env(safe-area-inset-bottom, 20px);
}

/* Utility classes */
.backface-hidden {
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
}

.card-face {
  @apply aspect-[11/19];
}

.reveal {
  background-image: url("/images/card-reveal.png");
  background-size: cover;
  background-position: center center;
}

.swiper-tinder-label {
  opacity: 0;
  transform: scale(0.8) rotate(-5deg);
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.swiper-slide-active.swiper-slide-swiping .swiper-tinder-label {
  opacity: 1;
  transform: scale(1.05) rotate(0deg);
}

.swiper-slide-active.swiper-slide-swiping-left .swiper-tinder-label-no {
  opacity: 1;
  transform: scale(1.1) rotate(-3deg);
  animation: bounceInLeft 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.swiper-slide-active.swiper-slide-swiping-right .swiper-tinder-label-yes {
  opacity: 1;
  transform: scale(1.1) rotate(3deg);
  animation: bounceInRight 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

/* Premium label animations */
@keyframes bounceInLeft {
  0% {
    opacity: 0;
    transform: scale(0.3) rotate(-15deg) translateX(-50px);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.15) rotate(-1deg) translateX(5px);
  }
  100% {
    opacity: 1;
    transform: scale(1.1) rotate(-3deg) translateX(0);
  }
}

@keyframes bounceInRight {
  0% {
    opacity: 0;
    transform: scale(0.3) rotate(15deg) translateX(50px);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.15) rotate(1deg) translateX(-5px);
  }
  100% {
    opacity: 1;
    transform: scale(1.1) rotate(3deg) translateX(0);
  }
}

/* Enhance the emoji icons */
.swiper-tinder-label .text-5xl,
.swiper-tinder-label .text-6xl,
.swiper-tinder-label .text-7xl {
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.4));
}

/* Slow bounce animation for emojis */
.animate-bounce-slow {
  animation: slowBounce 2s ease-in-out infinite;
}

@keyframes slowBounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

/* Enhanced label appearance on swipe */
.swiper-slide-active.swiper-slide-swiping-left .swiper-tinder-label-no {
  background: linear-gradient(
    135deg,
    rgba(239, 68, 68, 0.95),
    rgba(185, 28, 28, 0.95)
  ) !important;
}

.swiper-slide-active.swiper-slide-swiping-right .swiper-tinder-label-yes {
  background: linear-gradient(
    135deg,
    rgba(34, 197, 94, 0.95),
    rgba(21, 128, 61, 0.95)
  ) !important;
}

.pop-fade-enter-active {
  animation: pop-in 0.5s ease-out;
}

.pop-fade-leave-active,
.pop-fade-enter-active {
  transition: opacity 0.2s ease-out;
}

.pop-fade-enter-from,
.pop-fade-leave-to {
  opacity: 0;
}

@keyframes pop-in {
  0% {
    transform: scale(0);
    opacity: 0;
  }

  70% {
    transform: scale(1.1);
    opacity: 1;
  }

  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.icon-pop {
  animation: pop-in 0.3s ease-out;
}

.pop-fade-enter-active {
  animation: pop-in 0.3s ease-out;
}

.pop-fade-leave-active {
  animation: pop-out 0.2s ease-in;
}

@keyframes pop-out {
  from {
    transform: scale(1);
    opacity: 1;
  }

  to {
    transform: scale(0);
    opacity: 0;
  }
}

.slide-vertical-enter-active,
.slide-vertical-leave-active {
  transition: transform 0.3s ease-in-out;
}

.slide-vertical-enter-from,
.slide-vertical-leave-to {
  transform: translateY(-100%);
}

.slide-vertical-enter-to,
.slide-vertical-leave-from {
  transform: translateY(0);
}

/* Optional: Add a subtle scale effect for a more dynamic feel */
.slide-vertical-enter-active {
  transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out;
}

.slide-vertical-enter-from {
  transform: translateY(-100%) scale(0.95);
  opacity: 0;
}

.slide-vertical-enter-to {
  transform: translateY(0) scale(1);
  opacity: 1;
}

.card-container.is-flipped .card-face {
  z-index: 1;
  /* Keep front on top initially */
}

.card-container.is-flipped .card-back {
  z-index: 2;
  /* Ensure back face is on top after flip */
}

.card-text {
  br {
    @apply mb-2 block;
    content: "";
  }

  p {
    @apply mb-0;
  }
}

.mfa-reveal-card {
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  transform-style: preserve-3d;
}

.clip-diagonal {
  clip-path: polygon(
    0 0,
    100% 0,
    100% 100%,
    0 100%,
    0 0,
    85% 0,
    100% 15%,
    100% 100%,
    0 100%
  );
}

.mfa-reveal-card .card-face {
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.rotate-y-180 {
  transform: rotateY(180deg);
}

/* Swiper specific styles */
.swiper-slide-shadow {
  @apply absolute inset-0 bg-black bg-opacity-15 pointer-events-none z-10;
}

/* Safe area adjustment */
.pb-safe {
  padding-bottom: env(safe-area-inset-bottom, 20px);
}

.mfa-reveal-card .learning-objective {
  br {
    @apply mb-2 block;
    content: "";
  }

  p {
    @apply mb-0;
  }
}

.regular-reveal-card,
.is-flipped .card-face.front {
  background-image: url("/images/card-back.jpg");
  background-size: cover;
  background-position: center center;
}

/* Ensure MFA styles don't bleed into regular cards */
.card-face.back:not(.mfa-reveal-card) .absolute.inset-0.bg-opacity-90 {
  display: none;
}

/* Add this to your CSS */
swiper-container {
  perspective: 1000px;
}
</style>
