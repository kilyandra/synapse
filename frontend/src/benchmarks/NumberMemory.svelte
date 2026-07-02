<script>
  import { tick } from "svelte";
  import { saveResult, getBestResults, isLoggedIn } from "../lib/api.js";
  import PageTitle from "../lib/components/PageTitle.svelte";
  import Subtitle from "../lib/components/Subtitle.svelte";
  import Button from "../lib/components/Button.svelte";

  let status = $state(null);
  let level = $state(1);
  let number = $state("");
  let input = $state("");
  let best = $state(null);
  let inputRef = $state(null);
  let timer = undefined;

  $effect(() => {
    const cached = localStorage.getItem("best-results");
    if (cached) {
      const bests = JSON.parse(cached);
      const memory = bests.find((b) => b.benchmark === "number-memory");
      if (memory) best = memory.score;
    }

    if (isLoggedIn()) {
      getBestResults()
        .then((bests) => {
          localStorage.setItem("best-results", JSON.stringify(bests));
          const memory = bests.find((b) => b.benchmark === "number-memory");
          if (memory) best = memory.score;
        })
        .catch(() => {});
    }
  });

  function memorizeDuration(forLevel) {
    return 1000 + forLevel * 400;
  }

  function randomNumber(digits) {
    let n = String(Math.floor(Math.random() * 9) + 1);
    for (let i = 1; i < digits; i++) {
      n += String(Math.floor(Math.random() * 10));
    }
    return n;
  }

  function startLevel() {
    number = randomNumber(level);
    status = "memorize";
    timer = setTimeout(async () => {
      status = "recall";
      input = "";
      await tick();
      inputRef?.focus();
    }, memorizeDuration(level));
  }

  function finish(score) {
    if (score === 0) {
      status = null;
      return;
    }

    status = "done";

    if (isLoggedIn()) {
      saveResult("number-memory", score).catch(() => {});
    }

    if (best === null || score > best) {
      best = score;

      const cached = localStorage.getItem("best-results");
      const bests = cached ? JSON.parse(cached) : [];
      const index = bests.findIndex((b) => b.benchmark === "number-memory");
      if (index >= 0) {
        bests[index].score = score;
      } else {
        bests.push({ benchmark: "number-memory", score });
      }
      localStorage.setItem("best-results", JSON.stringify(bests));
    }
  }

  function checkAnswer() {
    if (input === number) {
      level += 1;
      startLevel();
    } else {
      finish(level - 1);
    }
  }

  function handleInput(e) {
    input = e.currentTarget.value.replace(/\D/g, "");
  }

  function handleKeydown(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      e.stopPropagation();
      checkAnswer();
    }
  }

  function restart() {
    level = 1;
    startLevel();
  }

  function handleZoneClick() {
    if (status === null) restart();
  }

  function handleZoneKeydown(e) {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      handleZoneClick();
    }
  }
</script>

<PageTitle>number memory</PageTitle>

<div class="h-full flex flex-col px-4 w-full mx-auto">
  <Subtitle
    >{#if best !== null}best: {best} digits{/if}</Subtitle
  >

  <div
    onclick={handleZoneClick}
    onkeydown={handleZoneKeydown}
    role="button"
    tabindex="0"
    class="flex-1 flex flex-col items-center pt-24 outline-none
           {status === null ? 'cursor-pointer' : ''}"
  >
    <div class="w-64">
      <div class="h-16 flex items-center justify-center">
        {#if status === "memorize"}
          <span class="text-4xl text-violet-600 tracking-widest">{number}</span>
        {:else if status === "recall"}
          <input
            bind:this={inputRef}
            type="text"
            inputmode="numeric"
            value={input}
            oninput={handleInput}
            onkeydown={handleKeydown}
            class="text-4xl text-violet-600 tracking-widest bg-transparent outline-none text-center w-full"
          />
        {:else if status === "done"}
          <span class="text-violet-600 text-2xl">{level - 1} digits</span>
        {/if}
      </div>

      <div class="h-1.5 rounded-full bg-violet-100 overflow-hidden">
        {#if status === "memorize"}
          {#key level}
            <div
              class="h-full bg-violet-600"
              style="animation: shrink-width {memorizeDuration(level)}ms linear forwards"
            ></div>
          {/key}
        {/if}
      </div>
    </div>

    <div class="mt-6 h-14 flex flex-col items-center gap-1">
      {#if status === "memorize"}
        <span class="text-neutral-700">memorize the number</span>
      {:else if status === "recall"}
        <span class="text-neutral-700">type what you saw</span>
      {:else if status === null}
        <span class="text-neutral-700">click to start</span>
      {/if}
    </div>

    {#if status === "memorize" || status === "recall"}
      <div class="mt-4">
        <Button variant={status === "recall" ? "primary" : "secondary"} onclick={checkAnswer}>
          check
        </Button>
      </div>
    {:else if status === "done"}
      <div class="mt-4">
        <Button variant="primary" onclick={restart}>restart</Button>
      </div>
    {/if}
  </div>
</div>
