<script>
  import { User, Settings, House } from "lucide-svelte";
  import { push } from "svelte-spa-router";
  import github from "../icons/github.svg";
  import NavButton from "./NavButton.svelte";

  let { children } = $props();
</script>

<div class="h-screen relative">
  <header class="fixed top-0 inset-x-0 z-10">
    <div class="px-4 pt-4 pb-2">
      <button
        onclick={() => push("/")}
        class="text-violet-600 text-2xl lg:text-3xl cursor-pointer"
      >
        synapse.
      </button>
    </div>
    <div class="h-2 bg-violet-600 rotate-[-2deg] scale-x-110"></div>
  </header>

  <main class="h-full overflow-y-auto pt-20 pb-24 flex">
    {@render children()}
  </main>

  <footer class="fixed bottom-0 inset-x-0 z-10">
    <div class="h-2 bg-violet-600 rotate-[-2deg] scale-x-110"></div>
    <nav class="flex items-end px-4 pt-4 pb-4">
      <a
        href="https://github.com/Kilyandra/synapse"
        target="_blank"
        class="flex items-baseline gap-1 mr-auto hover:underline"
      >
        <img src={github} alt="GitHub" class="w-4 h-4" />
        <span class="text-xs text-neutral-900">v{__APP_VERSION__}</span>
      </a>

      <div
        class="flex items-center w-fit h-12 rounded-2xl bg-white shadow-synapse"
      >
        <NavButton icon={User} path="/profile" />
        <NavButton icon={Settings} path="/settings" />
        <NavButton icon={House} path="/" />
      </div>
    </nav>
  </footer>
</div>
