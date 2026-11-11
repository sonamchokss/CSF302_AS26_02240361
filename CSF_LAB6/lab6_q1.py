"""CSF302 Lab 6, Question 1: rod cutting."""

import csv
import time
from pathlib import Path


PRICES = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]


def price(length):
    return PRICES[length] if length < len(PRICES) else 3 * length


def rod_cut_naive(n, counter):
    counter[0] += 1
    if n == 0:
        return 0
    return max(price(i) + rod_cut_naive(n - i, counter) for i in range(1, n + 1))


def rod_cut_memo(n, counter, memo=None):
    if memo is None:
        memo = {}
    counter[0] += 1
    if n in memo:
        return memo[n]
    if n == 0:
        memo[n] = 0
    else:
        memo[n] = max(
            price(i) + rod_cut_memo(n - i, counter, memo)
            for i in range(1, n + 1)
        )
    return memo[n]


def rod_cut_bottom_up(n, iterations=None):
    revenue = [0] * (n + 1)
    first_piece = [0] * (n + 1)
    if iterations is None:
        iterations = [0]
    for length in range(1, n + 1):
        best = -1
        for first in range(1, length + 1):
            iterations[0] += 1
            candidate = price(first) + revenue[length - first]
            if candidate > best:
                best = candidate
                first_piece[length] = first
        revenue[length] = best
    pieces = []
    remaining = n
    while remaining > 0:
        pieces.append(first_piece[remaining])
        remaining -= first_piece[remaining]
    return revenue[n], pieces


def run_benchmarks():
    rows = []
    for n in (5, 10, 15, 20, 25):
        counter = [0]
        start = time.perf_counter()
        naive_value = rod_cut_naive(n, counter)
        rows.append(["naive", n, naive_value, counter[0], time.perf_counter() - start])

        counter = [0]
        start = time.perf_counter()
        memo_value = rod_cut_memo(n, counter, {})
        rows.append(["memoized", n, memo_value, counter[0], time.perf_counter() - start])

        iterations = [0]
        start = time.perf_counter()
        bottom_value, _ = rod_cut_bottom_up(n, iterations)
        rows.append(["bottom-up", n, bottom_value, iterations[0], time.perf_counter() - start])
    return rows


def main():
    expected = [None, 1, 5, 8, 10, 13, 17, 18, 22, 25, 30]
    print("Q1 - Rod cutting")
    for n in range(1, 11):
        naive = rod_cut_naive(n, [0])
        memo = rod_cut_memo(n, [0], {})
        bottom, pieces = rod_cut_bottom_up(n)
        assert naive == memo == bottom == expected[n]
        print(f"n={n}: revenue={bottom}, pieces={pieces}")

    rows = run_benchmarks()
    output = Path(__file__).with_name("q1_results.csv")
    with output.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["method", "n", "revenue", "calls_or_iterations", "time_seconds"])
        writer.writerows(rows)
    print("\n| method | n | revenue | calls/iterations | time (s) |")
    print("|---|---:|---:|---:|---:|")
    for method, n, value, count, seconds in rows:
        print(f"| {method} | {n} | {value} | {count} | {seconds:.8f} |")
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
