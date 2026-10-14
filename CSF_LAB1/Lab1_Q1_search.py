import random
import time
import csv

random.seed(42)

def linear_search_361(arr_361, target_361):
    for i_361, val_361 in enumerate(arr_361):
        if val_361 == target_361:
            return i_361
    return -1

def binary_search_361(arr_361, target_361):
    lo_361, hi_361 = 0, len(arr_361) - 1
    while lo_361 <= hi_361:
        mid_361 = (lo_361 + hi_361) // 2
        if arr_361[mid_361] == target_361:
            return mid_361
        elif arr_361[mid_361] < target_361:
            lo_361 = mid_361 + 1
        else:
            hi_361 = mid_361 - 1
    return -1

INPUT_SIZES_361 = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
TRIALS_361 = 50  # number of search queries averaged per array size

def benchmark_361(size_361):
    # Generate a random dataset (unique values so search results are well-defined)
    data_361 = random.sample(range(size_361 * 10), size_361)
    sorted_data_361 = sorted(data_361)

    # Build query set: mix of present and guaranteed-absent values
    queries_361 = []
    for _ in range(TRIALS_361):
        if random.random() < 0.5:
            queries_361.append(random.choice(data_361))
        else:
            queries_361.append(-1)

    # Linear search timing (on unsorted data)
    start_361 = time.perf_counter()
    for q_361 in queries_361:
        linear_search_361(data_361, q_361)
    linear_time_361 = (time.perf_counter() - start_361) / TRIALS_361

    # Sort timing (needed before binary search)
    start_361 = time.perf_counter()
    sorted(data_361)
    sort_time_361 = time.perf_counter() - start_361

    # Binary search timing (on sorted data)
    start_361 = time.perf_counter()
    for q_361 in queries_361:
        binary_search_361(sorted_data_361, q_361)
    binary_time_361 = (time.perf_counter() - start_361) / TRIALS_361

    return linear_time_361, binary_time_361, sort_time_361

def main_361():
    results_361 = []
    print(f"{'Size':>10} | {'Linear (s)':>14} | {'Binary (s)':>14} | {'Sort (s)':>12} | {'Speedup':>10}")
    print("-" * 70)
    for size_361 in INPUT_SIZES_361:
        lt_361, bt_361, st_361 = benchmark_361(size_361)
        speedup_361 = lt_361 / bt_361 if bt_361 > 0 else float('inf')
        results_361.append({
            'size': size_361,
            'linear_time_s': lt_361,
            'binary_time_s': bt_361,
            'sort_time_s': st_361,
            'speedup': speedup_361
        })
        print(f"{size_361:>10} | {lt_361:>14.8f} | {bt_361:>14.8f} | {st_361:>12.6f} | {speedup_361:>10.1f}x")

    with open('q1_results.csv', 'w', newline='') as f_361:
        writer_361 = csv.DictWriter(f_361, fieldnames=['size', 'linear_time_s', 'binary_time_s', 'sort_time_s', 'speedup'])
        writer_361.writeheader()
        writer_361.writerows(results_361)
    print("\nSaved results to q1_results.csv")

if __name__ == '__main__':
    main_361()