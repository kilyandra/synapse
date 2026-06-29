import Home from './pages/Home.svelte'
import Benchmarks from './pages/Benchmarks.svelte'
import Settings from './pages/Settings.svelte'
import Profile from './pages/Profile.svelte'

export default {
  '/': Home,
  '/benchmarks': Benchmarks,
  '/settings': Settings,
  '/profile': Profile,
}