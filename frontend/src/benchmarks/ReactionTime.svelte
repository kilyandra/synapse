<script>
  import { saveResult, getBestResults, isLoggedIn } from "../lib/api.js";

  const TOTAL_ROUNDS = 5;

  let status = $state(null);
  let round = $state(0);
  let attempts = $state([]);
  let lastTime = $state(null);
  let result = $state(null);
  let best = $state(null);
  let startTime = null;
  let timer = undefined;
  let touchUsed = false;

  $effect(() => {
    if (isLoggedIn()) {
      const cached = localStorage.getItem("best-results");
      if (cached) {
        const bests = JSON.parse(cached);
        const reaction = bests.find((b) => b.benchmark === "reaction-time");
        if (reaction) best = reaction.score;
      }

      getBestResults()
        .then((bests) => {
          localStorage.setItem("best-results", JSON.stringify(bests));
          const reaction = bests.find((b) => b.benchmark === "reaction-time");
          if (reaction) best = reaction.score;
        })
        .catch(() => {});
    } else {
      const saved = localStorage.getItem("reaction-time");
      if (saved) best = Number(saved);
    }
  });

  function startRound() {
    status = "ready";
    const delay = 2000 + Math.random() * 3000;
    timer = setTimeout(() => {
      status = "go";
      startTime = Date.now();
    }, delay);
  }

  function finishTest() {
    const average = Math.round(
      attempts.reduce((sum, t) => sum + t, 0) / attempts.length,
    );
    result = average;
    status = "done";

    if (isLoggedIn()) {
      saveResult("reaction-time", average).catch(() => {});
      if (best === null || average < best) {
        best = average;

        const cached = localStorage.getItem("cached-best-results");
        const bests = cached ? JSON.parse(cached) : [];
        const index = bests.findIndex((b) => b.benchmark === "reaction-time");
        if (index >= 0) {
          bests[index].score = average;
        } else {
          bests.push({ benchmark: "reaction-time", score: average });
        }
        localStorage.setItem("cached-best-results", JSON.stringify(bests));
      }
    } else {
      if (best === null || average < best) {
        best = average;
        localStorage.setItem("best-reaction-time", String(best));
      }
    }
  }

  function handlePress(e) {
    //only left mouse button
    if (e.type === "mousedown" && e.button !== 0) {
      return;
    }

    if (e.type === "mousedown" && touchUsed) {
      touchUsed = false;
      return;
    }
    if (e.type === "touchstart") {
      touchUsed = true;
    }

    if (status === null || status === "done") {
      round = 1;
      attempts = [];
      result = null;
      lastTime = null;
      startRound();
      return;
    }

    if (status === "ready") {
      if (timer) clearTimeout(timer);
      round = 0;
      attempts = [];
      status = null;
      return;
    }

    if (status === "go") {
      const time = Date.now() - (startTime ?? 0);
      attempts = [...attempts, time];
      lastTime = time;

      if (round >= TOTAL_ROUNDS) {
        finishTest();
      } else {
        round += 1;
        startRound();
      }
    }
  }
</script>

<div class="h-full flex flex-col px-4 pt-6 w-full mx-auto">
  <p class="pb-2 text-2xl lg:text-3xl text-neutral-900 text-center">
    reaction time
  </p>

  <p class="h-5 text-sm text-neutral-400 text-center">
    {#if best !== null}best: {best} ms{/if}
  </p>

  <div
    onmousedown={handlePress}
    ontouchstart={handlePress}
    role="button"
    tabindex="0"
    class="flex-1 flex flex-col items-center cursor-pointer select-none pt-24"
  >
    <div
      class="w-40 h-40 rounded-2xl transition-colors shadow-synapse
                {status === 'go' ? 'bg-violet-600' : 'bg-white'}"
    ></div>

    <div class="mt-6 h-8 flex items-center">
      {#if status === null}
        <span class="text-neutral-700">click to start</span>
      {:else if status === "ready"}
        <span class="text-neutral-700">
          wait... ({round}/{TOTAL_ROUNDS})
          {#if lastTime !== null}
            <span class="text-sm text-neutral-400">{lastTime} ms</span>
          {/if}
        </span>
      {:else if status === "go"}
        <span class="text-violet-600">click!</span>
      {:else if status === "done"}
        <span class="text-violet-600 text-2xl">{result} ms</span>
      {/if}
    </div>
  </div>
</div>
