<script>
  import { User, Settings, House } from 'lucide-svelte'
  import { push, router } from 'svelte-spa-router'
  import github from '../icons/github.svg'
  
  let { children } = $props()
</script>

<div class="h-screen flex flex-col">

  <header class="px-4 pt-4 pb-2">
    <span class="text-violet-600 text-2xl">synapse.</span>
  </header>

  <div class="h-2 bg-violet-600 rotate-[-2deg] scale-x-110"></div>

  <main class="flex-1 flex">
    {@render children()}
  </main>

  <div class="h-2 bg-violet-600 rotate-[-2deg] scale-x-110"></div>

  <nav class="flex items-end px-4 pt-4 pb-4">
    <div class="flex items-baseline gap-1 mr-auto">
      <img src={github} alt="GitHub" class="w-5 h-5" />
      <span class="text-xs text-neutral-900">v{__APP_VERSION__}</span>
    </div>

    <div class="flex items-center w-fit h-12 rounded-2xl bg-white shadow-synapse gap-1">
      <button
        onclick={() => push('/profile')}
        class="w-12 h-12 flex items-center justify-center rounded-2xl
               {router.location === '/profile' ? 'bg-violet-600 text-white' : 'text-violet-600'}">
        <User size={32} />
      </button>
      <button
        onclick={() => push('/settings')}
        class="w-12 h-12 flex items-center justify-center rounded-2xl
               {router.location === '/settings' ? 'bg-violet-600 text-white' : 'text-violet-600'}">
        <Settings size={32} />
      </button>
      <button
        onclick={() => push('/')}
        class="w-12 h-12 flex items-center justify-center rounded-2xl
               {router.location === '/' ? 'bg-violet-600 text-white' : 'text-violet-600'}">
        <House size={32} />
      </button>
    </div>
  </nav>

</div>