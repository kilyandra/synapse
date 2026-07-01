<script>
  import Layout from "../lib/components/Layout.svelte";
  import { getBenchmarkComponent } from "../lib/benchmarks.js";

  let { params } = $props();
  let Component = $derived(getBenchmarkComponent(params.benchmark));
</script>

<Layout>
  <Component />
</Layout>
