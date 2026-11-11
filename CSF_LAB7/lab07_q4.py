"""CSF302 Lab 7, Question 4: randomized selection and Miller-Rabin."""

from __future__ import annotations

import csv
import math
import random
import time
from pathlib import Path


def quickselect(values: list[int], k: int, rng: random.Random | None = None) -> int:
    """Return the k-th smallest value, where k starts at one."""
    if not 1 <= k <= len(values):
        raise ValueError("k is out of range")
    rng = rng or random.Random()
    current = list(values)
    target = k - 1
    while True:
        pivot = current[rng.randrange(len(current))]
        lows = [value for value in current if value < pivot]
        equals = [value for value in current if value == pivot]
        if target < len(lows):
            current = lows
        elif target < len(lows) + len(equals):
            return pivot
        else:
            target -= len(lows) + len(equals)
            current = [value for value in current if value > pivot]


def mr_round(n: int, a: int) -> bool:
    """Run one Miller-Rabin round; True means probably prime."""
    if n < 2:
        return False
    exponent, odd_part = n - 1, 0
    while exponent % 2 == 0:
        exponent //= 2
        odd_part += 1
    value = pow(a, exponent, n)
    if value in (1, n - 1):
        return True
    for _ in range(odd_part - 1):
        value = value * value % n
        if value == n - 1:
            return True
    return False


def is_prime_mr(n: int, rounds: int = 20, rng: random.Random | None = None) -> bool:
    """Miller-Rabin with a small-prime pre-check."""
    if n < 2:
        return False
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n == prime:
            return True
        if n % prime == 0:
            return False
    rng = rng or random.Random()
    return all(mr_round(n, rng.randrange(2, n - 1)) for _ in range(rounds))


def trial_division(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def prime_samples(rng: random.Random, count: int) -> list[int]:
    values = []
    while len(values) < count:
        candidate = rng.randrange(10**11, 10**12)
        if is_prime_mr(candidate, 20, rng) and trial_division(candidate):
            values.append(candidate)
    return values


def time_call(function, values: list[int]) -> float:
    start = time.perf_counter()
    function(values)
    return time.perf_counter() - start


def run_experiments(seed: int = 302, output_csv: Path = Path("q4_timings.csv"), output_png: Path = Path("q4_timings.png")) -> None:
    rng = random.Random(seed)
    duplicate_values = [rng.randrange(10) for _ in range(200)]
    for k in (1, 100, 200) + tuple(rng.randint(1, 200) for _ in range(10)):
        assert quickselect(duplicate_values, k, rng) == sorted(duplicate_values)[k - 1]

    timing_rows = []
    for size in (10_000, 100_000, 1_000_000):
        values = [rng.randrange(1_000_000) for _ in range(size)]
        k = (size + 1) // 2
        for label in ("quickselect", "sorted"):
            measurements = []
            for _ in range(3):
                if label == "quickselect":
                    measurements.append(time_call(lambda data: quickselect(data, k, rng), values))
                else:
                    measurements.append(time_call(lambda data: sorted(data)[k - 1], values))
            timing_rows.append({"experiment": "selection", "size": size, "method": label, "seconds": sum(measurements) / len(measurements)})

    random_numbers = [rng.randrange(10**11, 10**12) for _ in range(20)]
    for number in random_numbers:
        assert is_prime_mr(number, 20, rng) == trial_division(number)
    primes = prime_samples(rng, 5)
    for number in range(0, 3000):
        assert is_prime_mr(number, 20, rng) == trial_division(number)
    timing_rows.extend(
        [
            {"experiment": "primality", "size": 20, "method": "Miller-Rabin random", "seconds": sum(time_call(lambda data: [is_prime_mr(n, 20, rng) for n in data], random_numbers) for _ in range(3)) / 3},
            {"experiment": "primality", "size": 5, "method": "trial division primes", "seconds": sum(time_call(lambda data: [trial_division(n) for n in data], primes) for _ in range(3)) / 3},
            {"experiment": "primality", "size": 5, "method": "Miller-Rabin primes", "seconds": sum(time_call(lambda data: [is_prime_mr(n, 20, rng) for n in data], primes) for _ in range(3)) / 3},
        ]
    )
    liar_count = sum(mr_round(561, rng.randrange(2, 560)) for _ in range(1000))
    with output_csv.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=timing_rows[0].keys())
        writer.writeheader()
        writer.writerows(timing_rows)
        writer.writerow({"experiment": "carmichael", "size": 1000, "method": "mr_round(561)", "seconds": liar_count / 1000})
    try:
        import matplotlib.pyplot as plt
        selection = [row for row in timing_rows if row["experiment"] == "selection"]
        plt.figure(figsize=(7, 4))
        for method in ("quickselect", "sorted"):
            subset = [row for row in selection if row["method"] == method]
            plt.plot([row["size"] for row in subset], [row["seconds"] for row in subset], marker="o", label=method)
        plt.xlabel("n")
        plt.ylabel("seconds")
        plt.title("Quickselect versus sorting")
        plt.legend()
        plt.tight_layout()
        plt.savefig(output_png, dpi=150)
        plt.close()
    except ImportError:
        print("matplotlib is not installed; timing CSV was still written.")
    print("12-digit primes:", primes)
    print("561 accepted in one round:", liar_count, "/ 1000")


if __name__ == "__main__":
    run_experiments()
