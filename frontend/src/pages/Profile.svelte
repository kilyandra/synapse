<script>
  import Layout from "../lib/components/Layout.svelte";
  import Button from "../lib/components/Button.svelte";
  import PageContent from "../lib/components/PageContent.svelte";
  import PageTitle from "../lib/components/PageTitle.svelte";
  import Subtitle from "../lib/components/Subtitle.svelte";
  import TextInput from "../lib/components/TextInput.svelte";
  import { register, login, getMe, logout } from "../lib/api.js";
  import validator from "validator";

  let user = $state(null);
  let checkingAuth = $state(true);

  function setUser(u) {
    user = u;
    localStorage.setItem("cached-user", JSON.stringify(u));
  }

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
        setUser(u);
        checkingAuth = false;
      })
      .catch(() => {
        logout();
        user = null;
        checkingAuth = false;
      });
  });

  let mode = $state("login");
  let email = $state("");
  let password = $state("");
  let error = $state("");
  let submitting = $state(false);
  let passwordInput = $state(null);

  function handleEmailKeydown(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      passwordInput?.focus();
    }
  }

  function handlePasswordKeydown(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSubmit();
    }
  }

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
      setUser(u);
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
  <PageTitle>profile</PageTitle>
  {#if !checkingAuth && !user}
    <Subtitle>log in to track your scores</Subtitle>
  {/if}
  <PageContent>
    {#if user}
      <div class="bg-white card p-6 w-full max-w-sm flex flex-col gap-2">
        <p class="text-violet-600 text-xl">{user.username}</p>
        <p class="text-neutral-500 text-sm">{user.email}</p>
      </div>
      <div class="flex justify-center pt-4">
        <Button variant="primary" onclick={handleLogout}>logout</Button>
      </div>
    {:else if !checkingAuth}
      <div class="w-full max-w-sm flex flex-col gap-3 pt-12">
        <TextInput
          type="email"
          bind:value={email}
          disabled={submitting}
          onkeydown={handleEmailKeydown}
        />
        <TextInput
          type="password"
          bind:value={password}
          disabled={submitting}
          onkeydown={handlePasswordKeydown}
          bind:inputRef={passwordInput}
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
  </PageContent>
</Layout>
