<script>
  import Layout from "../lib/components/Layout.svelte";
  import Button from "../lib/components/Button.svelte";
  import PageContent from "../lib/components/PageContent.svelte";
  import PageTitle from "../lib/components/PageTitle.svelte";
  import Subtitle from "../lib/components/Subtitle.svelte";
  import TextInput from "../lib/components/TextInput.svelte";
  import { register, login, getMe, logout, getAuthConfig, googleAuth } from "../lib/api.js";
  import validator from "validator";

  let user = $state(null);
  let checkingAuth = $state(true);
  let googleClientId = $state(null);
  let googleContainer = $state(null);
  let googleAvailable = $state(true);

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

  $effect(() => {
    if (checkingAuth || user) return;

    getAuthConfig()
      .then((config) => {
        googleClientId = config.google_client_id;
      })
      .catch(() => {});
  });

  function loadGoogleScript() {
    if (window.google?.accounts?.id) return Promise.resolve();

    const existing = document.getElementById("google-identity-script");
    if (existing) {
      return new Promise((resolve, reject) => {
        existing.addEventListener("load", resolve, { once: true });
        existing.addEventListener("error", reject, { once: true });
      });
    }

    return new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.id = "google-identity-script";
      script.src = "https://accounts.google.com/gsi/client?hl=en";
      script.async = true;
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  async function handleGoogleCredential(response) {
    error = "";
    submitting = true;
    try {
      await googleAuth(response.credential);
      const u = await getMe();
      setUser(u);
    } catch (e) {
      error = e.message;
    } finally {
      submitting = false;
    }
  }

  async function initGoogleButton() {
    try {
      await loadGoogleScript();
      window.google.accounts.id.initialize({
        client_id: googleClientId,
        callback: handleGoogleCredential,
      });
      window.google.accounts.id.renderButton(googleContainer, {
        theme: "outline",
        size: "large",
        width: 320,
        text: "continue_with",
      });

      setTimeout(() => {
        if (googleContainer && googleContainer.childElementCount === 0) {
          googleAvailable = false;
        }
      }, 3000);
    } catch {
      googleAvailable = false;
    }
  }

  $effect(() => {
    if (!googleClientId || !googleContainer) return;
    initGoogleButton();
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
        <div class="w-full flex flex-col items-center gap-3 min-h-18 justify-center">
          {#if googleClientId && googleAvailable}
            <div class="flex justify-center w-full" bind:this={googleContainer}></div>
            <div class="flex items-center gap-2 text-xs text-neutral-400 w-full">
              <div class="flex-1 h-px bg-neutral-200"></div>
              or
              <div class="flex-1 h-px bg-neutral-200"></div>
            </div>
          {/if}
        </div>

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
