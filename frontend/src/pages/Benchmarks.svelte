<script>
  import Layout from '../lib/components/Layout.svelte'
  import { Zap, Binary, Clock } from 'lucide-svelte'
  import BenchmarkCard from '../lib/components/BenchmarkCard.svelte';
</script>

<Layout>
  <div class="h-full flex flex-col px-4 pt-6 gap-6 w-full mx-auto">
    <p class="text-2xl lg:text-3xl text-neutral-900 text-center">benchmarks</p>

    <div class="flex flex-wrap justify-center gap-4 px-4 pt-2 w-full max-w-4xl mx-auto">
      <BenchmarkCard icon={Zap} name="reaction time" path="/bm/reaction-time" />
      <BenchmarkCard icon={Binary} name="number memory" path="/bm/number-memory" />
      <BenchmarkCard icon={Clock} name="placeholder" />

    </div>
  </div>
</Layout>