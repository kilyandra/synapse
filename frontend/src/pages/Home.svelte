<script>
  import Layout from "../lib/components/Layout.svelte";
  import Button from "../lib/components/Button.svelte";
  import { push } from "svelte-spa-router";
</script>

<Layout>
  <div class="flex-1 flex flex-col items-center justify-center gap-2">
    <p class="text-neutral-900 text-2xl lg:text-3xl pb-6">
      benchmark yourself.
    </p>
    <Button onclick={() => push("/bm")}>begin</Button>
    <Button variant="secondary" onclick={() => {}}>compete</Button>
    <div class="h-35"></div>
  </div>
</Layout>
