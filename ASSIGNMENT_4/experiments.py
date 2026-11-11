"""Small experiments for the hall-booking assignment."""

import csv
import random

from booking import (best_schedule, brute_force, greedy_earliest_finish,
                     greedy_highest_fee)


def show_counterexample(requests):
    """Print all algorithm results for one hand-made example."""
    print("Requests:", requests)
    for name, function in [
        ("greedy_earliest_finish", greedy_earliest_finish),
        ("greedy_highest_fee", greedy_highest_fee),
        ("best_schedule", best_schedule),
        ("brute_force", brute_force),
    ]:
        print(f"{name}: {function(requests)}")


def random_requests(rng, count, start_max, duration_min, duration_max,
                    fee_min, fee_max):
    """Generate valid requests using the documented parameter ranges."""
    requests = []
    for _ in range(count):
        start = rng.randint(0, start_max)
        duration = rng.randint(duration_min, duration_max)
        requests.append((start, start + duration,
                         rng.randint(fee_min, fee_max)))
    return requests


def ratio_experiment():
    """Run two 1000-trial ratio experiments and save every trial to CSV."""
    generators = [
        ("standard", 100, 1, 20, 100, 1000),
        ("short_durations", 100, 1, 5, 100, 1000),
    ]
    rows = []
    summary = []
    for name, start_max, duration_min, duration_max, fee_min, fee_max in generators:
        rng = random.Random(20261103)
        ratios = {"earliest_finish": [], "highest_fee": []}
        for trial in range(1000):
            requests = random_requests(
                rng, 50, start_max, duration_min, duration_max,
                fee_min, fee_max)
            optimum = best_schedule(requests)[0]
            for rule, function in [
                ("earliest_finish", greedy_earliest_finish),
                ("highest_fee", greedy_highest_fee),
            ]:
                total = function(requests)[0]
                ratio = total / optimum
                ratios[rule].append(ratio)
                rows.append([name, trial, rule, total, optimum, ratio])
        for rule, values in ratios.items():
            summary.append((name, rule, sum(values) / len(values), min(values)))

    with open("booking_ratios.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["generator", "trial", "rule", "greedy_total",
                         "optimal_total", "ratio"])
        writer.writerows(rows)

    print("| Generator | Rule | Average ratio | Worst ratio |")
    print("|---|---|---:|---:|")
    for name, rule, average, worst in summary:
        print(f"| {name} | {rule} | {average:.4f} | {worst:.4f} |")


if __name__ == "__main__":
    show_counterexample([(9, 12, 3000), (10, 16, 8000), (13, 17, 4000),
                         (12, 14, 2500), (16, 18, 2000)])
    ratio_experiment()

