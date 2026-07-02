const API_URL = "/api";
const REQUEST_TIMEOUT_MS = 10000;

export async function apiRequest(path, options = {}) {
  const token = localStorage.getItem("token");
  const headers = { "Content-Type": "application/json", ...options.headers };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  let res;
  try {
    res = await fetch(`${API_URL}${path}`, {
      ...options,
      headers,
      signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
    });
  } catch (e) {
    throw new Error(e.name === "TimeoutError" ? "request timed out" : "network error");
  }

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    const message =
      typeof error.detail === "string" ? error.detail : `request failed: ${res.status}`;
    throw new Error(message);
  }

  if (res.status === 204) return null;

  return res.json();
}

export async function register(email, password) {
  const data = await apiRequest("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  localStorage.setItem("token", data.access_token);
  await syncLocalBestResults();
  return data;
}

export async function login(email, password) {
  const data = await apiRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  localStorage.setItem("token", data.access_token);
  await syncLocalBestResults();
  return data;
}

export async function getMe() {
  return apiRequest("/auth/me");
}

export async function getAuthConfig() {
  return apiRequest("/auth/config");
}

export async function googleAuth(credential) {
  const data = await apiRequest("/auth/google", {
    method: "POST",
    body: JSON.stringify({ credential }),
  });
  localStorage.setItem("token", data.access_token);
  await syncLocalBestResults();
  return data;
}

export function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("cached-user");
  localStorage.removeItem("best-results");
}

export async function saveResult(benchmark, score) {
  return apiRequest("/results", {
    method: "POST",
    body: JSON.stringify({ benchmark, score }),
  });
}

export async function checkResults(results) {
  return apiRequest("/results/check", {
    method: "POST",
    body: JSON.stringify(results),
  });
}

async function syncLocalBestResults() {
  const cached = localStorage.getItem("best-results");
  const localBests = cached ? JSON.parse(cached) : [];
  if (localBests.length === 0) return;

  try {
    const merged = await checkResults(localBests);
    localStorage.setItem("best-results", JSON.stringify(merged));
  } catch {
    // best effort — при неудаче следующий заход на страницу теста всё равно подтянет /results/best
  }
}

export async function getBestResults() {
  return apiRequest("/results/best");
}

export function isLoggedIn() {
  return !!localStorage.getItem("token");
}
