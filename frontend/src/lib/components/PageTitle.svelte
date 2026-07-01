<script>
  let { children } = $props();
</script>

<p class="text-2xl lg:text-3xl text-neutral-900 text-center pt-6 pb-2 items-center">
  {@render children()}
</p>
