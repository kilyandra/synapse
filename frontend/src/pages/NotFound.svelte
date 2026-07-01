<script>
  import Layout from "../lib/components/Layout.svelte";
  import Button from "../lib/components/Button.svelte";
  import { navigate } from "../lib/router.svelte.js";
</script>

<Layout>
  <div class="flex-1 flex flex-col items-center justify-center gap-4">
    <p class="text-neutral-900 text-2xl lg:text-3xl">
      404
    </p>
    <p class="text-neutral-500 text-sm">this page doesn't exist</p>
    <Button onclick={() => navigate("/")}>back home</Button>
    <div class="h-35"></div>
  </div>
</Layout>
