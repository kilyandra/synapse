<script>
  import { routerState } from "./lib/router.svelte.js";
  import Home from "./pages/Home.svelte";
  import Benchmarks from "./pages/Benchmarks.svelte";
  import Settings from "./pages/Settings.svelte";
  import Profile from "./pages/Profile.svelte";
  import BenchmarkRunner from "./pages/BenchmarkRunner.svelte";

  let path = $derived(routerState.path);
  let test = $derived(path.startsWith("/bm/") ? path.slice(4) : null);
</script>

{#if path === "/"}
  <Home />
{:else if path === "/bm"}
  <Benchmarks />
{:else if path === "/settings"}
  <Settings />
{:else if path === "/profile"}
  <Profile />
{:else if test}
  <BenchmarkRunner params={{ test }} />
{:else}
  <p>404</p>
{/if}
