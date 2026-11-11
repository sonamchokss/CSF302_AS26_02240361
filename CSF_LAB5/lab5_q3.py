"""CSF302 Lab 5, Question 3: inversion counts and Kendall tau distance."""

import csv
import random
import time
from pathlib import Path


def brute_force_inversions(values):
    total = 0
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] > values[j]:
                total += 1
    return total


def merge_count_inversions(values):
    def sort_and_count(items):
        if len(items) <= 1:
            return list(items), 0
        middle = len(items) // 2
        left, left_count = sort_and_count(items[:middle])
        right, right_count = sort_and_count(items[middle:])
        merged, i, j, cross_count = [], 0, 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                cross_count += len(left) - i
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, left_count + right_count + cross_count

    return sort_and_count(values)[1]


def kendall_tau_from_ranks(ranks_a, ranks_b):
    order_a = sorted(range(len(ranks_a)), key=lambda index: ranks_a[index])
    ranks_in_a_order = [ranks_b[index] for index in order_a]
    distance = merge_count_inversions(ranks_in_a_order)
    pairs = len(ranks_a) * (len(ranks_a) - 1) // 2
    coefficient = 1 - (2 * distance / pairs)
    percentage = 100 * (1 - distance / pairs)
    return distance, percentage, coefficient


def _read_ranking(user_name, titles):
    while True:
        try:
            values = [int(input(f"{user_name}, rank for {title}: ")) for title in titles]
            if sorted(values) != list(range(1, len(titles) + 1)):
                raise ValueError
            return values
        except ValueError:
            print("Enter each whole-number rank from 1 to 10 exactly once.")


def ranking_program():
    titles = [input(f"Movie {i + 1} title: ") for i in range(10)]
    ranks_a = _read_ranking("User A", titles)
    ranks_b = _read_ranking("User B", titles)
    distance, percentage, coefficient = kendall_tau_from_ranks(ranks_a, ranks_b)
    print(f"Kendall tau distance: {distance} / 45")
    print(f"Similarity: {percentage:.2f}%")
    print(f"Kendall tau coefficient: {coefficient:.4f}")


def benchmark(output_path=None):
    output_path = Path(output_path or Path(__file__).with_name("q3_results.csv"))
    rng = random.Random(361)
    rows = []
    brute_previous = None
    for n in [1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000, 512000, 1000000]:
        values = [rng.randrange(100) for _ in range(n)]
        row = {"n": n}
        if brute_previous is not None and brute_previous > 60:
            row["brute_time_seconds"] = "stopped"
        else:
            start = time.perf_counter()
            brute_force_inversions(values)
            brute_time = time.perf_counter() - start
            row["brute_time_seconds"] = brute_time
            brute_previous = brute_time * 4
            if brute_time > 60:
                row["brute_time_seconds"] = "stopped"
        start = time.perf_counter()
        fast_count = merge_count_inversions(values)
        row["merge_time_seconds"] = time.perf_counter() - start
        row["merge_count"] = fast_count
        assert fast_count == merge_count_inversions(values)
        if n <= 2000:
            assert fast_count == brute_force_inversions(values)
        rows.append(row)
    with output_path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    _plot(rows, output_path.with_name("q3_times.png"))
    print("n, brute time, merge time, inversion count")
    for row in rows:
        print(row)


def _plot(rows, output_path):
    import matplotlib.pyplot as plt
    usable = [row for row in rows if isinstance(row["brute_time_seconds"], float)]
    plt.figure()
    plt.loglog([row["n"] for row in usable],
               [row["brute_time_seconds"] for row in usable], "o-", label="brute force")
    plt.loglog([row["n"] for row in rows],
               [row["merge_time_seconds"] for row in rows], "o-", label="merge-based")
    plt.xlabel("n")
    plt.ylabel("time (seconds)")
    plt.title("Lab 5 Question 3 inversion-count times")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def correctness_checks():
    rng = random.Random(361)
    for n in [0, 1, 10, 100, 2000]:
        values = [rng.randrange(10) for _ in range(n)]
        assert merge_count_inversions(values) == brute_force_inversions(values)
    for n in [10, 100]:
        assert merge_count_inversions(list(range(n))) == 0
        assert merge_count_inversions(list(range(n, 0, -1))) == n * (n - 1) // 2
    assert kendall_tau_from_ranks(list(range(1, 11)), list(range(1, 11)))[0] == 0
    assert kendall_tau_from_ranks(list(range(1, 11)), list(range(10, 0, -1)))[0] == 45
    print("Correctness checks passed, including duplicate-heavy arrays and Kendall tau extremes.")


if __name__ == "__main__":
    correctness_checks()
    benchmark()
