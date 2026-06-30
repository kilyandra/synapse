export const routerState = $state({ path: window.location.pathname })

export function navigate(to) {
    window.history.pushState({}, '', to)
    routerState.path = to
}

window.addEventListener('popstate', () => {
    routerState.path = window.location.pathname
})
