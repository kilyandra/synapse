<script>
  import Layout from "../lib/components/Layout.svelte";
  import Button from "../lib/components/Button.svelte";
  import { register, login, getMe, logout } from "../lib/api.js";

  let mode = $state("login");
  let email = $state("");
  let password = $state("");
  let error = $state("");
  let user = $state(null);
  let loading = $state(true);

  $effect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      getMe()
        .then((u) => (user = u))
        .catch(() => logout())
        .finally(() => (loading = false));
    } else {
      loading = false;
    }
  });

  function validate() {
    if (!email.trim() || !password.trim()) {
      error = "fill in all fields";
      return false;
    }
    // простая проверка email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      error = "invalid email";
      return false;
    }
    if (password.length < 8) {
      error = "password must be at least 8 characters";
      return false;
    }
    return true;
  }

  async function handleSubmit() {
    error = "";
    if (!validate()) return;

    loading = true;
    try {
      if (mode === "login") {
        await login(email, password);
      } else {
        await register(email, password);
      }
      user = await getMe();
      email = "";
      password = "";
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  function handleLogout() {
    logout();
    user = null;
  }
</script>

<Layout>
  <div class="h-full flex flex-col px-4 pt-6 w-full mx-auto">
    <p class="pb-2 text-2xl lg:text-3xl text-neutral-900 text-center">
      profile
    </p>

    {#if !loading && !user}
      <p class="h-5 text-sm text-neutral-400 text-center">
        log in to track your scores
      </p>
    {/if}

    <div class="flex-1 flex flex-col items-center pt-12 gap-4">
      {#if loading}
        <p class="text-neutral-400 text-sm">loading...</p>
      {:else if user}
        <div
          class="bg-white shadow-synapse rounded-2xl p-6 w-full max-w-sm flex flex-col gap-2"
        >
          <p class="text-violet-600 text-xl">{user.username}</p>
          <p class="text-neutral-500 text-sm">{user.email}</p>
        </div>
        <div class="flex justify-center pt-4">
          <Button variant="primary" onclick={handleLogout}>logout</Button>
        </div>
      {:else}
        <div class="w-full max-w-sm flex flex-col gap-3 pt-12">
          <input
            type="email"
            placeholder="email"
            bind:value={email}
            class="bg-white shadow-synapse rounded-2xl px-4 py-3 outline-none"
          />
          <input
            type="password"
            placeholder="password"
            bind:value={password}
            class="bg-white shadow-synapse rounded-2xl px-4 py-3 outline-none"
          />

          {#if error}
            <p class="text-red-500 text-sm text-center">{error}</p>
          {/if}

          <div class="flex justify-center pt-4">
            <Button onclick={handleSubmit}>
              {mode === "login" ? "login" : "register"}
            </Button>
          </div>

          <button
            onclick={() => {
              mode = mode === "login" ? "register" : "login";
              email = "";
              password = "";
              error = "";
            }}
            class="text-sm text-neutral-500 hover:text-violet-600 cursor-pointer"
          >
            {mode === "login" ? "no account? register" : "have account? login"}
          </button>
        </div>
      {/if}
    </div>
  </div>
</Layout>
