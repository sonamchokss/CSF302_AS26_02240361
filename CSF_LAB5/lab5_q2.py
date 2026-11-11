"""CSF302 Lab 5, Question 2: stable counting sort and LSD radix sort."""

import csv
import random
import time
from pathlib import Path

try:
    from lab01 import merge_sort
except ImportError:
    try:
        from Lab1_Q2_sort import merge_sort_361 as merge_sort
    except ImportError:
        def merge_sort(values):
            """Fallback; replace this with the Lab 1 merge_sort if available."""
            if len(values) <= 1:
                return list(values)
            middle = len(values) // 2
            left = merge_sort(values[:middle])
            right = merge_sort(values[middle:])
            result, i, j = [], 0, 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            return result + left[i:] + right[j:]


def counting_sort(values, key=lambda value: value, maximum=None):
    """Stable counting sort for non-negative integer keys."""
    items = list(values)
    if not items:
        return []
    keys = [key(item) for item in items]
    maximum = max(keys) if maximum is None else maximum
    counts = [0] * (maximum + 1)
    for item_key in keys:
        if item_key < 0 or item_key > maximum:
            raise ValueError("counting-sort key is outside 0..maximum")
        counts[item_key] += 1
    for index in range(1, len(counts)):
        counts[index] += counts[index - 1]
    result = [None] * len(items)
    for item, item_key in reversed(list(zip(items, keys))):
        counts[item_key] -= 1
        result[counts[item_key]] = item
    return result


def radix_sort(values, base=10):
    result = list(values)
    if not result:
        return result
    if min(result) < 0:
        raise ValueError("radix_sort accepts non-negative integers")
    place = 1
    maximum = max(result)
    while place <= maximum:
        # Bind place and base now; this avoids late binding in callbacks.
        result = counting_sort(
            result, key=lambda value, p=place, b=base: (value // p) % b,
            maximum=base - 1,
        )
        place *= base
    return result


def stability_demo():
    pairs = [(2, "first 2"), (1, "one"), (2, "second 2"), (0, "zero")]
    stable = counting_sort(pairs, key=lambda pair: pair[0])
    forward = _unstable_forward_counting_sort(pairs, lambda pair: pair[0])
    assert [pair[1] for pair in stable if pair[0] == 2] == ["first 2", "second 2"]
    assert [pair[1] for pair in forward if pair[0] == 2] != ["first 2", "second 2"]
    print("Stable example:", stable)
    print("Forward-placement example (not stable):", forward)


def _unstable_forward_counting_sort(values, key):
    items = list(values)
    maximum = max(key(item) for item in items)
    counts = [0] * (maximum + 1)
    for item in items:
        counts[key(item)] += 1
    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]
    result = [None] * len(items)
    for item in items:
        item_key = key(item)
        counts[item_key] -= 1
        result[counts[item_key]] = item
    return result


def benchmark(output_dir=None):
    output_dir = Path(output_dir or Path(__file__).parent)
    rng = random.Random(361)
    count_rows = []
    n = 100_000
    for k in [10, 10**3, 10**5, 10**7]:
        values = [rng.randrange(k + 1) for _ in range(n)]
        start = time.perf_counter()
        answer = counting_sort(values, maximum=k)
        count_time = time.perf_counter() - start
        assert answer == sorted(values)
        start = time.perf_counter()
        baseline = merge_sort(values)
        merge_time = time.perf_counter() - start
        assert baseline == answer
        count_rows.append({"n": n, "k": k, "counting_time": count_time,
                           "merge_time": merge_time})
    radix_rows = []
    for n in [10_000, 100_000, 500_000, 1_000_000]:
        values = [rng.randrange(10**9 + 1) for _ in range(n)]
        row = {"n": n, "k": 10**9}
        for base in [10, 256]:
            start = time.perf_counter()
            answer = radix_sort(values, base=base)
            row[f"radix_{base}_time"] = time.perf_counter() - start
            assert answer == sorted(values)
            row[f"radix_{base}_passes"] = len(str(10**9)) if base == 10 else 4
        start = time.perf_counter()
        answer = merge_sort(values)
        row["merge_time"] = time.perf_counter() - start
        assert answer == sorted(values)
        radix_rows.append(row)
    with (output_dir / "q2_counting_results.csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=count_rows[0].keys())
        writer.writeheader()
        writer.writerows(count_rows)
    with (output_dir / "q2_radix_results.csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=radix_rows[0].keys())
        writer.writeheader()
        writer.writerows(radix_rows)
    _plot(radix_rows, output_dir / "q2_radix_times.png")
    _plot(count_rows, output_dir / "q2_counting_times.png", x_key="k")
    print("Counting-sort rows:", count_rows)
    print("Radix-sort rows:", radix_rows)


def _plot(rows, output_path, x_key="n"):
    import matplotlib.pyplot as plt
    plt.figure()
    for key in rows[0]:
        if key.endswith("_time") and key != "time_seconds":
            plt.loglog([row[x_key] for row in rows], [row[key] for row in rows],
                       marker="o", label=key)
    plt.xlabel(x_key)
    plt.ylabel("time (seconds)")
    plt.title("Lab 5 Question 2 sorting times")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


if __name__ == "__main__":
    stability_demo()
    benchmark()
