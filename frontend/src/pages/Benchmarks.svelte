<script>
  import Layout from "../lib/components/Layout.svelte";
  import { Zap, Binary, Clock } from "lucide-svelte";
  import BenchmarkCard from "../lib/components/BenchmarkCard.svelte";
  import PageContent from "../lib/components/PageContent.svelte";
  import PageTitle from "../lib/components/PageTitle.svelte";
</script>

<Layout>
  <PageTitle>benchmarks</PageTitle>
  <PageContent>
    <div class="flex flex-wrap justify-center gap-4 px-4 pt-2 w-full max-w-4xl mx-auto">
      <BenchmarkCard icon={Zap} name="reaction time" path="/bm/reaction-time" />
      <BenchmarkCard icon={Binary} name="number memory" />
      <BenchmarkCard icon={Clock} name="placeholder" />
    </div>
  </PageContent>
</Layout>
