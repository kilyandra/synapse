<script>
  import { routerState } from "./lib/router.svelte.js";
  import { BENCHMARKS } from "./lib/benchmarks.js";
  import Home from "./pages/Home.svelte";
  import Benchmarks from "./pages/Benchmarks.svelte";
  import Settings from "./pages/Settings.svelte";
  import Profile from "./pages/Profile.svelte";
  import BenchmarkRunner from "./pages/BenchmarkRunner.svelte";
  import NotFound from "./pages/NotFound.svelte";

  let path = $derived(routerState.path.replace(/\/+$/, "") || "/");
  let benchmark = $derived(path.startsWith("/bm/") ? path.slice(4) : null);
  let isKnownBenchmark = $derived(benchmark !== null && BENCHMARKS.includes(benchmark));
</script>

{#if path === "/"}
  <Home />
{:else if path === "/bm"}
  <Benchmarks />
{:else if path === "/settings"}
  <Settings />
{:else if path === "/profile"}
  <Profile />
{:else if isKnownBenchmark}
  <BenchmarkRunner params={{ benchmark }} />
{:else}
  <NotFound />
{/if}
