<script>
  import { push } from "svelte-spa-router";
  let { icon: Icon, name, path = null } = $props();
</script>

<button
  onclick={() => path && push(path)}
  disabled={!path}
  class="bg-white shadow-synapse rounded-2xl flex flex-col w-35 aspect-[5/4] transition-all duration-200
         {path
    ? 'hover:bg-violet-50 hover:-translate-y-1 cursor-pointer'
    : 'opacity-50 cursor-default'}"
>
  <div class="pt-4 flex justify-center">
    <Icon class="w-12 h-12 text-violet-600" />
  </div>
  <div class="px-3 pb-4 pt-2">
    <span class="text-sm leading-snug block">{name}</span>
  </div>
</button>
