"""Benchmark, CSV, and graph generation for the two quicksorts."""

import csv
import multiprocessing
import random
import statistics
import time

import matplotlib.pyplot as plt

from sorts import quicksort_basic, quicksort_improved


TIME_LIMIT = 60.0
SIZES = [1000 * (2 ** exponent) for exponent in range(7)]
INPUT_TYPES = ("random", "sorted", "duplicates")


def _sort_worker(values, algorithm, cutoff, result_connection):
    """Sort a private copy and send either time or an exception name."""
    data = values[:]
    start = time.perf_counter()
    try:
        if algorithm == "basic":
            quicksort_basic(data)
        else:
            quicksort_improved(data, cutoff)
    except RecursionError:
        result_connection.send(("RecursionError", None))
        result_connection.close()
        return
    result_connection.send(("ok", time.perf_counter() - start))
    result_connection.close()


def timed_run(values, algorithm, cutoff=None, limit=TIME_LIMIT):
    """Run one fresh-copy timing with a hard wall-clock limit."""
    parent_connection, child_connection = multiprocessing.Pipe()
    process = multiprocessing.Process(
        target=_sort_worker,
        args=(values, algorithm, cutoff, child_connection),
    )
    process.start()
    child_connection.close()
    deadline = time.perf_counter() + limit
    while time.perf_counter() < deadline:
        if parent_connection.poll(0.05):
            status, seconds = parent_connection.recv()
            process.join(1)
            parent_connection.close()
            return status if status != "ok" else seconds
        if not process.is_alive():
            break
    if process.is_alive():
        process.terminate()
        process.join()
        parent_connection.close()
        return "stopped"
    if not parent_connection.poll(1):
        parent_connection.close()
        return "stopped"
    status, seconds = parent_connection.recv()
    parent_connection.close()
    return status if status != "ok" else seconds


def repetitions_for(size):
    """Use several measurements for small inputs and fewer for large ones."""
    if size <= 4000:
        return 5
    if size <= 16000:
        return 3
    return 1


def make_input(kind, size, rng):
    if kind == "random":
        return [rng.randint(-1_000_000, 1_000_000) for _ in range(size)]
    if kind == "sorted":
        return list(range(size))
    return [rng.randint(0, 9) for _ in range(size)]


def mean_numeric(results):
    numbers = [value for value in results if isinstance(value, float)]
    if numbers:
        return statistics.mean(numbers)
    if "RecursionError" in results:
        return "RecursionError"
    return "stopped"


def print_timing_table(kind, rows):
    print(f"\n### {kind.title()} input")
    print("| n | basic seconds/status | improved seconds |")
    print("|---:|---:|---:|")
    for row in rows:
        print(f"| {row['n']} | {row['basic']} | {row['improved']} |")


def save_graph(kind, rows):
    numeric_basic = [(row["n"], row["basic"]) for row in rows if isinstance(row["basic"], float)]
    numeric_improved = [(row["n"], row["improved"]) for row in rows if isinstance(row["improved"], float)]
    plt.figure()
    if numeric_basic:
        plt.loglog(*zip(*numeric_basic), "o-", label="Basic quicksort")
    if numeric_improved:
        plt.loglog(*zip(*numeric_improved), "o-", label="Improved quicksort")
    plt.xlabel("Input size n (transactions)")
    plt.ylabel("Time (seconds)")
    plt.title(f"Quicksort timing: {kind} input")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"benchmark_{kind}.png", dpi=150)
    plt.close()


def cutoff_experiment(rng):
    """Measure cutoffs on 100,000 random values and print the winner."""
    values = [rng.randint(-1_000_000, 1_000_000) for _ in range(100_000)]
    rows = []
    for cutoff in (1, 4, 8, 16, 32, 64):
        measurements = [
            timed_run(values, "improved", cutoff, TIME_LIMIT)
            for _ in range(5)
        ]
        numbers = [value for value in measurements if isinstance(value, float)]
        mean = statistics.mean(numbers) if numbers else float("inf")
        median = statistics.median(numbers) if numbers else float("inf")
        spread = max(numbers) - min(numbers) if numbers else float("inf")
        rows.append((cutoff, mean, median, spread))
    best_mean = min(row[1] for row in rows)
    print("\n### Cutoff experiment (n = 100000)")
    print("| cutoff | mean seconds | median seconds | spread |")
    print("|---:|---:|---:|---:|")
    for cutoff, mean, median, spread in rows:
        mark = " **best**" if mean == best_mean else ""
        noisy = " (within 5% noise)" if mean <= best_mean * 1.05 else ""
        print(f"| {cutoff} | {mean:.6f} | {median:.6f} | {spread:.6f}{mark}{noisy} |")
    return min(rows, key=lambda row: row[1])[0]


def compare_with_sorted(rng, cutoff):
    print("\n### Best quicksort versus sorted() (n = 100000)")
    print("| input | quicksort seconds | sorted seconds | sorted/quicksort |")
    print("|---|---:|---:|---:|")
    for kind in INPUT_TYPES:
        values = make_input(kind, 100_000, rng)
        quick_times = [timed_run(values, "improved", cutoff) for _ in range(3)]
        sorted_times = []
        for _ in range(3):
            data = values[:]
            start = time.perf_counter()
            sorted(data)
            sorted_times.append(time.perf_counter() - start)
        builtin = statistics.mean(sorted_times)
        numeric_quick = [value for value in quick_times if isinstance(value, float)]
        if numeric_quick:
            quick = statistics.mean(numeric_quick)
            ratio = f"{builtin / quick:.3f}"
            quick_text = f"{quick:.6f}"
        else:
            ratio = "not available"
            quick_text = quick_times[-1]
        print(f"| {kind} | {quick_text} | {builtin:.6f} | {ratio} |")


def main():
    rng = random.Random(20261103)
    all_rows = []
    for kind in INPUT_TYPES:
        rows = []
        for size in SIZES:
            values = make_input(kind, size, rng)
            repeats = repetitions_for(size)
            basic = mean_numeric([timed_run(values, "basic") for _ in range(repeats)])
            improved = mean_numeric([timed_run(values, "improved", 16) for _ in range(repeats)])
            rows.append({"input": kind, "n": size, "basic": basic, "improved": improved})
            all_rows.append(rows[-1])
        print_timing_table(kind, rows)
        save_graph(kind, rows)

        print(f"\nDoubling ratios for {kind}:")
        for previous, current in zip(rows, rows[1:]):
            basic_ratio = (
                "not available"
                if not isinstance(previous["basic"], float) or not isinstance(current["basic"], float)
                else f"{current['basic'] / previous['basic']:.3f}"
            )
            improved_ratio = (
                "not available"
                if not isinstance(previous["improved"], float) or not isinstance(current["improved"], float)
                else f"{current['improved'] / previous['improved']:.3f}"
            )
            print(f"{current['n']}/{previous['n']}: basic={basic_ratio}, improved={improved_ratio}")

    with open("results.csv", "w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=["input", "n", "basic", "improved"])
        writer.writeheader()
        writer.writerows(all_rows)

    best_cutoff = cutoff_experiment(rng)
    print(f"\nChosen best cutoff from this run: {best_cutoff}")
    compare_with_sorted(rng, best_cutoff)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
