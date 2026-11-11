"""Benchmark closest-pair algorithms and create a log-log graph."""

import csv
import random
import time
import timeit

import matplotlib.pyplot as plt

from closest import closest_pair, closest_pair_brute


def average_time(function, points, repetitions):
    """Return average seconds for repeated calls."""
    start = time.perf_counter()
    for _ in range(repetitions):
        function(points)
    elapsed = time.perf_counter() - start
    return elapsed / repetitions


def find_crossover():
    """Return the first n with five consecutive D&C wins."""
    recent_wins = []
    for count in range(2, 301):
        points = [(index * 0.37, (index * 17) % 31) for index in range(count)]
        repetitions = max(10, min(1000, 20000 // count))
        brute_runs = timeit.repeat(
            lambda: closest_pair_brute(points),
            repeat=3,
            number=repetitions,
        )
        divide_runs = timeit.repeat(
            lambda: closest_pair(points),
            repeat=3,
            number=repetitions,
        )
        brute_time = min(brute_runs) / repetitions
        divide_time = min(divide_runs) / repetitions
        recent_wins.append(divide_time < brute_time)
        if len(recent_wins) >= 5 and all(recent_wins[-5:]):
            return count - 4
    return None


def main():
    """Run the requested benchmark and save its files."""
    # Use one seed so the benchmark can be repeated.
    rng = random.Random(20261103)
    # These are 1000, 2000, ..., 64000.
    sizes = [1000 * (2 ** exponent) for exponent in range(7)]
    rows = []
    brute_stopped = False

    for count in sizes:
        # Both algorithms receive this exact same list.
        points = [
            (rng.uniform(-1000, 1000), rng.uniform(-1000, 1000))
            for _ in range(count)
        ]
        # Average several quick D&C runs.
        divide_repetitions = 5 if count <= 4000 else 3
        divide_seconds = average_time(closest_pair, points, divide_repetitions)

        # Stop brute force after a run takes more than 60 seconds.
        if brute_stopped:
            brute_seconds = "stopped"
        else:
            start = time.perf_counter()
            closest_pair_brute(points)
            brute_seconds = time.perf_counter() - start
            if brute_seconds > 60:
                brute_stopped = True
                brute_seconds = "stopped"

        # Calculate the comparison ratio when both times exist.
        if brute_seconds == "stopped":
            ratio = "stopped"
        else:
            ratio = brute_seconds / divide_seconds
        rows.append((count, brute_seconds, divide_seconds, ratio))

    # Print a Markdown timing table.
    print("| n | brute seconds | D&C seconds | brute/D&C ratio |")
    print("|---:|---:|---:|---:|")
    for count, brute, divide, ratio in rows:
        print(f"| {count} | {brute} | {divide:.6f} | {ratio} |")

    # Save the same values as CSV.
    with open("results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["n", "brute_seconds", "divide_conquer_seconds", "ratio"])
        writer.writerows(rows)

    # Plot only numeric brute-force values.
    numeric_rows = [row for row in rows if row[1] != "stopped"]
    plt.figure()
    plt.loglog(
        [row[0] for row in numeric_rows],
        [row[1] for row in numeric_rows],
        "o-",
        label="Brute force",
    )
    plt.loglog(
        [row[0] for row in rows],
        [row[2] for row in rows],
        "o-",
        label="Divide and conquer",
    )
    plt.xlabel("Input size n (points)")
    plt.ylabel("Time (seconds)")
    plt.title("Closest-pair running time")
    plt.legend()
    plt.tight_layout()
    plt.savefig("timing.png", dpi=150)
    plt.close()

    # Print the crossover result.
    print("\nCrossover n:", find_crossover())
    print("Crossover rule: five consecutive D&C wins using the fastest of three repeats.")

    # Print time(2n) / time(n) for each available adjacent pair.
    print("\nDoubling ratios:")
    for index in range(1, len(rows)):
        previous = rows[index - 1]
        current = rows[index]
        if previous[1] == "stopped" or current[1] == "stopped":
            brute_ratio = "stopped"
        else:
            brute_ratio = current[1] / previous[1]
        divide_ratio = current[2] / previous[2]
        print(f"{current[0]}/{previous[0]}: brute={brute_ratio}, D&C={divide_ratio:.3f}")


if __name__ == "__main__":
    main()
