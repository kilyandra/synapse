const API_URL = '/api'

export async function apiRequest(path, options = {}) {
    const token = localStorage.getItem('token')
    const headers = { 'Content-Type': 'application/json', ...options.headers }
    if (token) headers['Authorization'] = `Bearer ${token}`

    const res = await fetch(`${API_URL}${path}`, { ...options, headers })

    if (!res.ok) {
        const error = await res.json().catch(() => ({}))
        throw new Error(error.detail || `Request failed: ${res.status}`)
    }

    if (res.status === 204) return null

    return res.json()
}

export async function register(email, password) {
    const data = await apiRequest('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
    })
    localStorage.setItem('token', data.access_token)
    return data
}

export async function login(email, password) {
    const data = await apiRequest('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
    })
    localStorage.setItem('token', data.access_token)
    return data
}

export async function getMe() {
    return apiRequest('/auth/me')
}

export function logout() {
    localStorage.removeItem('token')
}

export async function saveResult(benchmark, score) {
    return apiRequest('/results', {
        method: 'POST',
        body: JSON.stringify({ benchmark, score }),
    })
}

export async function getBestResults() {
    return apiRequest('/results/best')
}

export function isLoggedIn() {
    return !!localStorage.getItem('token')
}
