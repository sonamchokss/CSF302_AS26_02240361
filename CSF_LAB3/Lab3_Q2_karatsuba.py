"""
Q2: Karatsuba's Algorithm for Large Integer Multiplication
"""

import time
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------- Helpers: represent big numbers as digit lists (least-significant first) ----------

def random_digits(num_digits):
    if num_digits == 1:
        return random.randint(0, 9)
    first = random.randint(1, 9)
    rest = [random.randint(0, 9) for _ in range(num_digits - 1)]
    return int(str(first) + ''.join(map(str, rest)))


def to_digit_list(x):
    if x == 0:
        return [0]
    s = str(x)
    return [int(c) for c in reversed(s)]


def from_digit_list(d):
    s = ''.join(str(dig) for dig in reversed(d))
    s = s.lstrip('0')
    return int(s) if s else 0


def pad_to_length(d, length):
    return d + [0] * (length - len(d))


def next_power_of_2(n):
    p = 1
    while p < n:
        p *= 2
    return p


# ---------- 1) Traditional grade-school multiplication O(n^2) ----------

def traditional_multiply(x, y):
    dx = to_digit_list(x)
    dy = to_digit_list(y)
    n, m = len(dx), len(dy)
    result = [0] * (n + m)

    for i in range(n):
        carry = 0
        for j in range(m):
            result[i + j] += dx[i] * dy[j] + carry
            carry = result[i + j] // 10
            result[i + j] %= 10
        result[i + m] += carry

    return from_digit_list(result)


# ---------- 2) Karatsuba's algorithm O(n^1.585) ----------

def karatsuba(x, y):
    if x < 10 or y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))
    n = next_power_of_2(n)
    half = n // 2

    high_x, low_x = divmod(x, 10 ** half)
    high_y, low_y = divmod(y, 10 ** half)

    z0 = karatsuba(low_x, low_y)  
    z2 = karatsuba(high_x, high_y)               
    z1 = karatsuba(low_x + high_x, low_y + high_y) - z2 - z0  

    return z2 * 10 ** (2 * half) + z1 * 10 ** half + z0


# ---------- Experiment: correctness + timing comparison ----------

def run_comparison(digit_sizes=(8, 16, 32, 64, 128, 256, 512, 1024), trials=1, seed=42):
    random.seed(seed)
    results = []
    print(f"{'digits':>7} | {'Traditional (s)':>16} | {'Karatsuba (s)':>14} | {'Match?':>7}")
    print("-" * 55)

    for d in digit_sizes:
        trad_times, kara_times = [], []
        match = True
        for _ in range(trials):
            x = random_digits(d)
            y = random_digits(d)

            t0 = time.perf_counter()
            r_trad = traditional_multiply(x, y)
            t1 = time.perf_counter()
            trad_times.append(t1 - t0)

            t0 = time.perf_counter()
            r_kara = karatsuba(x, y)
            t1 = time.perf_counter()
            kara_times.append(t1 - t0)

            if r_trad != r_kara:
                match = False

        avg_trad = sum(trad_times) / trials
        avg_kara = sum(kara_times) / trials
        results.append((d, avg_trad, avg_kara, match))
        print(f"{d:>7} | {avg_trad:16.6f} | {avg_kara:14.6f} | {str(match):>7}")

    return results


def plot_results(results, filename="karatsuba_time_comparison.png"):
    ds = [r[0] for r in results]
    trad = [r[1] for r in results]
    kara = [r[2] for r in results]

    plt.figure(figsize=(8, 5.5))
    plt.plot(ds, trad, marker='o', label='Traditional O(n^2)')
    plt.plot(ds, kara, marker='s', label="Karatsuba O(n^1.585)")
    plt.xlabel("Number of digits (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Large Integer Multiplication: Traditional vs Karatsuba")
    plt.xscale('log', base=2)
    plt.yscale('log')
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"\nGraph saved as {filename}")


if __name__ == "__main__":
    # Small manual demo
    x, y = 1234, 5678
    print(f"x = {x}, y = {y}")
    print("Traditional:", traditional_multiply(x, y))
    print("Karatsuba:  ", karatsuba(x, y))
    print("Actual (x*y):", x * y)

    print("\n=== Timing comparison: Traditional vs Karatsuba ===")
    results = run_comparison(digit_sizes=(8, 16, 32, 64, 128, 256, 512, 1024))
    plot_results(results)
