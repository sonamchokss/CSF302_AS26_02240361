"""CSF302 Lab 5, Question 1: quicksort variants and measurements."""

import csv
import math
import multiprocessing
import random
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Stats:
    comparisons: int = 0


def lomuto_partition(a, low, high, stats):
    pivot = a[high]
    i = low
    for j in range(low, high):
        stats.comparisons += 1
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[high] = a[high], a[i]
    return i


def hoare_partition(a, low, high, stats, pivot_choice):
    pivot_index = low if pivot_choice == "first" else (low + high) // 2
    pivot = a[pivot_index]
    i, j = low - 1, high + 1
    while True:
        while True:
            i += 1
            stats.comparisons += 1
            if a[i] >= pivot:
                break
        while True:
            j -= 1
            stats.comparisons += 1
            if a[j] <= pivot:
                break
        if i >= j:
            return j
        a[i], a[j] = a[j], a[i]


def _quicksort_lomuto(a, low, high, stats):
    while low < high:
        split = lomuto_partition(a, low, high, stats)
        if split - low < high - split:
            _quicksort_lomuto(a, low, split - 1, stats)
            low = split + 1
        else:
            _quicksort_lomuto(a, split + 1, high, stats)
            high = split - 1


def _quicksort_hoare(a, low, high, stats, pivot_choice):
    while low < high:
        split = hoare_partition(a, low, high, stats, pivot_choice)
        if split - low < high - split:
            _quicksort_hoare(a, low, split, stats, pivot_choice)
            low = split + 1
        else:
            _quicksort_hoare(a, split + 1, high, stats, pivot_choice)
            high = split


def _quicksort_three_way(a, low, high, stats):
    while low < high:
        pivot = a[high]
        less, scan, greater = low, low, high
        while scan <= greater:
            stats.comparisons += 1
            if a[scan] < pivot:
                a[less], a[scan] = a[scan], a[less]
                less += 1
                scan += 1
            else:
                stats.comparisons += 1
                if a[scan] > pivot:
                    a[scan], a[greater] = a[greater], a[scan]
                    greater -= 1
                else:
                    scan += 1
        if less - low < high - greater:
            _quicksort_three_way(a, low, less - 1, stats)
            low = greater + 1
        else:
            _quicksort_three_way(a, greater + 1, high, stats)
            high = less - 1


def _randomized_lomuto(a, low, high, stats, rng):
    while low < high:
        pivot_index = rng.randint(low, high)
        a[pivot_index], a[high] = a[high], a[pivot_index]
        split = lomuto_partition(a, low, high, stats)
        if split - low < high - split:
            _randomized_lomuto(a, low, split - 1, stats, rng)
            low = split + 1
        else:
            _randomized_lomuto(a, split + 1, high, stats, rng)
            high = split - 1


def sort_with_stats(values, variant, rng=None):
    a = list(values)
    stats = Stats()
    if len(a) > 1:
        if variant == "lomuto":
            _quicksort_lomuto(a, 0, len(a) - 1, stats)
        elif variant.startswith("hoare_"):
            _quicksort_hoare(a, 0, len(a) - 1, stats, variant[6:])
        elif variant == "randomized":
            _randomized_lomuto(a, 0, len(a) - 1, stats, rng or random.Random(0))
        elif variant == "three_way":
            _quicksort_three_way(a, 0, len(a) - 1, stats)
        else:
            raise ValueError("unknown quicksort variant")
    return a, stats.comparisons


VARIANTS = ["lomuto", "hoare_first", "hoare_middle", "randomized", "three_way"]
INPUT_TYPES = ["random", "sorted", "reverse", "duplicates"]
SIZES = [1000, 2000, 4000, 8000, 16000]


def make_input(kind, n, seed):
    rng = random.Random(seed)
    if kind == "random":
        return [rng.randrange(10 * n) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "reverse":
        return list(range(n, 0, -1))
    return [rng.randrange(10) for _ in range(n)]


def run_experiments(output_path=None):
    output_path = Path(output_path or Path(__file__).with_name("q1_results.csv"))
    rows = []
    for input_type in INPUT_TYPES:
        for n in SIZES:
            values = make_input(input_type, n, 361 + n)
            repeats = 3 if n <= 4000 else 1
            for variant in VARIANTS:
                comparison_runs, time_runs = [], []
                for trial in range(repeats):
                    result = _run_with_timeout(
                        values, variant, 5, 9000 + trial
                    )
                    if result is None:
                        comparison_runs = ["stopped"]
                        time_runs = ["stopped"]
                        break
                    verified, comparisons, elapsed = result
                    assert verified
                    comparison_runs.append(comparisons)
                    time_runs.append(elapsed)
                comparisons = comparison_runs[-1]
                seconds = time_runs[-1]
                rows.append({
                    "input_type": input_type,
                    "n": n,
                    "variant": variant,
                    "comparisons": comparisons,
                    "time_seconds": seconds,
                    "comparisons_over_n_log2_n": (
                        comparisons / (n * math.log2(n))
                        if isinstance(comparisons, int) else "stopped"
                    ),
                    "comparisons_over_n_squared": (
                        comparisons / (n * n)
                        if isinstance(comparisons, int) else "stopped"
                    ),
                    "repeats": repeats,
                })
    with output_path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print_markdown_tables(rows)
    print(f"Saved {output_path}")
    return rows


def _timed_sort(values, variant, seed, queue):
    start = time.perf_counter()
    result, comparisons = sort_with_stats(values, variant, random.Random(seed))
    queue.put((result == sorted(values), comparisons, time.perf_counter() - start))


def _run_with_timeout(values, variant, timeout, seed):
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=_timed_sort, args=(values, variant, seed, queue)
    )
    process.start()
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        process.join()
        return None
    return queue.get() if not queue.empty() else None


def print_markdown_tables(rows):
    for input_type in INPUT_TYPES:
        print(f"\n### {input_type.title()} inputs: comparisons")
        print("| n | variant | comparisons | count/(n log2 n) | count/n^2 |")
        print("|---:|---|---:|---:|---:|")
        for row in rows:
            if row["input_type"] == input_type:
                print(
                    f"| {row['n']} | {row['variant']} | {row['comparisons']} | "
                    f"{row['comparisons_over_n_log2_n']} | "
                    f"{row['comparisons_over_n_squared']} |"
                )
        print(f"\n### {input_type.title()} inputs: times")
        print("| n | variant | time (seconds) | repeats |")
        print("|---:|---|---:|---:|")
        for row in rows:
            if row["input_type"] == input_type:
                print(
                    f"| {row['n']} | {row['variant']} | "
                    f"{row['time_seconds']} | {row['repeats']} |"
                )


if __name__ == "__main__":
    run_experiments()
