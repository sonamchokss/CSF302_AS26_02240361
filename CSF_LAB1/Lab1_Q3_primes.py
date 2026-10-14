import time
import csv
import math

def is_prime_naive_361(n_361):
    if n_361 < 2:
        return False
    for i_361 in range(2, n_361):
        if n_361 % i_361 == 0:
            return False
    return True

def naive_trial_division_361(limit_361):
    return [n_361 for n_361 in range(2, limit_361 + 1) if is_prime_naive_361(n_361)]

def is_prime_optimized_361(n_361):
    if n_361 < 2:
        return False
    if n_361 < 4:
        return True
    if n_361 % 2 == 0:
        return False
    for i_361 in range(3, int(math.isqrt(n_361)) + 1, 2):
        if n_361 % i_361 == 0:
            return False
    return True

def optimized_trial_division_361(limit_361):
    return [n_361 for n_361 in range(2, limit_361 + 1) if is_prime_optimized_361(n_361)]

def sieve_of_eratosthenes_361(limit_361):
    is_prime_361 = bytearray([1]) * (limit_361 + 1)
    is_prime_361[0:2] = b'\x00\x00'
    for i_361 in range(2, int(math.isqrt(limit_361)) + 1):
        if is_prime_361[i_361]:
            is_prime_361[i_361*i_361:limit_361+1:i_361] = bytearray(len(range(i_361*i_361, limit_361 + 1, i_361)))
    return [i_361 for i_361, p_361 in enumerate(is_prime_361) if p_361]

INPUT_SIZES_361 = [10_000, 50_000, 100_000, 500_000, 1_000_000]
NAIVE_MAX_361 = 100_000  # naive is O(n^2/ln n); capped to keep runtime reasonable

def main_361():
    results_361 = []
    print(f"{'N':>10} | {'Naive (s)':>14} | {'Optimized (s)':>14} | {'Sieve (s)':>12} | {'#Primes':>10}")
    print("-" * 75)
    for n_361 in INPUT_SIZES_361:
        row_361 = {'n': n_361}

        if n_361 <= NAIVE_MAX_361:
            start_361 = time.perf_counter()
            primes_naive_361 = naive_trial_division_361(n_361)
            row_361['naive_time_s'] = time.perf_counter() - start_361
        else:
            row_361['naive_time_s'] = None

        start_361 = time.perf_counter()
        primes_opt_361 = optimized_trial_division_361(n_361)
        row_361['optimized_time_s'] = time.perf_counter() - start_361

        start_361 = time.perf_counter()
        primes_sieve_361 = sieve_of_eratosthenes_361(n_361)
        row_361['sieve_time_s'] = time.perf_counter() - start_361

        row_361['num_primes'] = len(primes_sieve_361)

        assert len(primes_opt_361) == len(primes_sieve_361)
        if row_361['naive_time_s'] is not None:
            assert len(primes_naive_361) == len(primes_sieve_361)

        results_361.append(row_361)
        naive_str_361 = f"{row_361['naive_time_s']:.6f}" if row_361['naive_time_s'] is not None else "skipped"
        print(f"{n_361:>10} | {naive_str_361:>14} | {row_361['optimized_time_s']:>14.6f} | {row_361['sieve_time_s']:>12.6f} | {row_361['num_primes']:>10}")

    with open('q3_results.csv', 'w', newline='') as f_361:
        writer_361 = csv.DictWriter(f_361, fieldnames=['n', 'naive_time_s', 'optimized_time_s', 'sieve_time_s', 'num_primes'])
        writer_361.writeheader()
        writer_361.writerows(results_361)
    print("\nSaved results to q3_results.csv")

if __name__ == '__main__':
    main_361()