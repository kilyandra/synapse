<script>
  import Layout from "../lib/components/Layout.svelte";
  import Button from "../lib/components/Button.svelte";
  import { navigate } from "../lib/router.svelte.js";
  import PageContent from "../lib/components/PageContent.svelte";
  import PageTitle from "../lib/components/PageTitle.svelte";
</script>

<Layout>
  <PageContent center>
    <PageTitle>404</PageTitle>
    <Button onclick={() => navigate("/")}>back home</Button>
  </PageContent>
</Layout>
