<script>
  import Layout from "../lib/components/Layout.svelte";
  import Button from "../lib/components/Button.svelte";
  import { register, login, getMe, logout } from "../lib/api.js";
  import validator from "validator";

  let mode = $state("login");
  let email = $state("");
  let password = $state("");
  let error = $state("");
  let user = $state(null);
  let checkingAuth = $state(true);
  let submitting = $state(false);

  $effect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      checkingAuth = false;
      return;
    }

    const cached = localStorage.getItem("cached-user");
    if (cached) {
      user = JSON.parse(cached);
      checkingAuth = false;
    }

    getMe()
      .then((u) => {
        user = u;
        localStorage.setItem("cached-user", JSON.stringify(u));
        checkingAuth = false;
      })
      .catch(() => {
        logout();
        user = null;
        checkingAuth = false;
      });
  });

  function validate() {
    if (!email.trim() || !password.trim()) {
      error = "fill in all fields";
      return false;
    }

    if (!validator.isEmail(email)) {
      error = "please enter a valid email address";
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

    submitting = true;
    try {
      if (mode === "login") {
        await login(email, password);
      } else {
        await register(email, password);
      }
      const u = await getMe();
      user = u;
      localStorage.setItem("cached-user", JSON.stringify(u));
      email = "";
      password = "";
    } catch (e) {
      error = e.message;
    } finally {
      submitting = false;
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

    {#if !checkingAuth && !user}
      <p class="h-5 text-sm text-neutral-400 text-center">
        log in to track your scores
      </p>
    {/if}

    <div class="flex-1 flex flex-col items-center pt-12 gap-4">
      {#if user}
        <div
          class="bg-white shadow-synapse rounded-2xl p-6 w-full max-w-sm flex flex-col gap-2"
        >
          <p class="text-violet-600 text-xl">{user.username}</p>
          <p class="text-neutral-500 text-sm">{user.email}</p>
        </div>
        <div class="flex justify-center pt-4">
          <Button variant="primary" onclick={handleLogout}>logout</Button>
        </div>
      {:else if !checkingAuth}
        <div class="w-full max-w-sm flex flex-col gap-3 pt-12">
          <input
            type="email"
            placeholder="email"
            bind:value={email}
            disabled={submitting}
            class="bg-white shadow-synapse rounded-2xl px-4 py-3 outline-none disabled:opacity-50"
          />
          <input
            type="password"
            placeholder="password"
            bind:value={password}
            disabled={submitting}
            class="bg-white shadow-synapse rounded-2xl px-4 py-3 outline-none disabled:opacity-50"
          />

          <p class="h-5 text-red-500 text-sm text-center">{error}</p>

          <div class="flex justify-center pt-4">
            <Button onclick={handleSubmit} disabled={submitting}>
              {submitting ? "..." : mode === "login" ? "login" : "register"}
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
