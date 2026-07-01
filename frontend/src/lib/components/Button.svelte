<script>
  let { children, variant = "primary", onclick = () => {} } = $props();
</script>

<button
  {onclick}
  disabled={variant === "secondary"}
  class="w-40 h-10 text-base card transition-colors
         {variant === 'primary'
    ? 'bg-violet-600 hover:bg-violet-700 text-white cursor-pointer'
    : 'bg-violet-100 text-violet-300 cursor-default'}"
>
  {@render children()}
</button>
