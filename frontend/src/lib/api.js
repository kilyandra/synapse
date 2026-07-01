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
    const message = parseErrorDetail(error.detail) || `Request failed: ${res.status}`;
    throw new Error(message);
  }

  if (res.status === 204) return null;

  return res.json();
}

function parseErrorDetail(detail) {
  if (!detail) return null;
  if (typeof detail === "string") return detail;

  if (Array.isArray(detail)) {
    const first = detail[0];
    if (!first) return "validation error";

    if (first.loc?.includes("email")) {
      return "please enter a valid email address";
    }

    if (first.loc?.includes("password")) {
      return "password must be at least 8 characters";
    }

    return "invalid input";
  }

  return null;
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
