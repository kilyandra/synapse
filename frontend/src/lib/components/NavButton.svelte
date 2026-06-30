<script>
  import { navigate, routerState } from "../router.svelte.js";
  let { icon: Icon, path } = $props();
</script>

<button
  onclick={() => navigate(path)}
  class="w-12 h-12 flex items-center justify-center rounded-2xl
         {routerState.path === path
    ? 'bg-violet-600 text-white'
    : 'text-violet-600 hover:bg-violet-100 cursor-pointer'}"
>
  <Icon size={32} />
</button>
