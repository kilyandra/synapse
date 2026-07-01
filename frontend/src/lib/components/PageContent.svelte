<script>
  let { children, center = false } = $props();
</script>

<div
  class="w-full flex flex-col items-center
  {center ? 'flex-1 justify-center gap-2' : 'h-full px-4 pt-6 gap-6'}"
>
  {@render children()}
</div>
