BENCHMARKS = {
    "reaction-time": "min",
    "number-memory": "max",
}

def is_better(benchmark: str, new_score: int, old_score: int) -> bool:
    direction = BENCHMARKS.get(benchmark, "min")
    if direction == "min":
        return new_score < old_score
    return new_score > old_score


def benchmark_exists(benchmark: str) -> bool:
    return benchmark in BENCHMARKS
