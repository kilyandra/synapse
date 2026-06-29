import Home from './pages/Home.svelte'
import Benchmarks from './pages/Benchmarks.svelte'
import Settings from './pages/Settings.svelte'
import Profile from './pages/Profile.svelte'
import BenchmarkRunner from './pages/BenchmarkRunner.svelte'

export default {
  '/': Home,
  '/bm': Benchmarks,
  '/settings': Settings,
  '/profile': Profile,
  '/bm/:test': BenchmarkRunner,
}