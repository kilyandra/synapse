<script>
  let { children, variant = "primary", onclick } = $props();
</script>

<button
  {onclick}
  class="w-40 h-10 text-base shadow-synapse rounded-2xl transition-colors cursor-pointer
         {variant === 'primary'
    ? 'bg-violet-600 hover:bg-violet-700 text-white'
    : 'bg-violet-100 text-violet-300'}"
>
  {@render children()}
</button>
