<script>
  import Layout from '../lib/components/Layout.svelte'
  import ReactionTime from '../benchmarks/ReactionTime.svelte'
  
  let { params } = $props()
</script>

<Layout>
  {#if params.test === 'reaction-time'}
    <ReactionTime />
  {:else}
    <div class="h-full flex items-center justify-center">
      <p>test not found: {params.test}</p>
    </div>
  {/if}
</Layout>