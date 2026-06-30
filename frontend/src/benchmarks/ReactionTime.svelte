<script>
  import { saveResult, getBestResults, isLoggedIn } from "../lib/api.js";

  let status = $state(null);
  let result = $state(null);
  let best = $state(null);
  let startTime = null;
  let timer = undefined;
  let touchUsed = false;

  $effect(() => {
    if (isLoggedIn()) {
      getBestResults()
        .then((bests) => {
          const reaction = bests.find((b) => b.benchmark === "reaction-time");
          if (reaction) best = reaction.score;
        })
        .catch(() => {});
    } else {
      const saved = localStorage.getItem("best-reaction-time");
      if (saved) best = Number(saved);
    }
  });

  function handlePress(e) {
    if (e.type === "mousedown" && touchUsed) {
      touchUsed = false;
      return;
    }
    if (e.type === "touchstart") {
      touchUsed = true;
    }

    if (status === null) {
      status = "ready";
      result = null;
      const delay = 2000 + Math.random() * 3000;
      timer = setTimeout(() => {
        status = "go";
        startTime = Date.now();
      }, delay);
      return;
    }

    if (status === "ready") {
      if (timer) clearTimeout(timer);
      status = null;
      result = null;
      return;
    }

    if (status === "go") {
      result = Date.now() - (startTime ?? 0);

      if (isLoggedIn()) {
        saveResult("reaction-time", result).catch(() => {});
        if (best === null || result < best) {
          best = result;
        }
      } else {
        if (best === null || result < best) {
          best = result;
          localStorage.setItem("best-reaction-time", String(best));
        }
      }

      status = null;
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
    class="flex-1 flex flex-col items-center cursor-pointer select-none pt-32"
  >
    <div
      class="w-40 h-40 rounded-2xl transition-colors shadow-synapse
                {status === 'go' ? 'bg-violet-600' : 'bg-white'}"
    ></div>

    <div class="mt-6 h-8 flex items-center">
      {#if status === null && result}
        <span class="text-violet-600 text-2xl">{result} ms</span>
      {:else if status === null}
        <span class="text-neutral-700">click to start</span>
      {:else if status === "ready"}
        <span class="text-neutral-700">wait...</span>
      {:else if status === "go"}
        <span class="text-violet-600">click!</span>
      {/if}
    </div>
  </div>
</div>
