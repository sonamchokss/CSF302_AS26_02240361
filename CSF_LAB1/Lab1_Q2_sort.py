import random
import time
import csv

random.seed(42)

def bubble_sort_361(arr_361):
    a_361 = arr_361[:]
    n_361 = len(a_361)
    for i_361 in range(n_361 - 1):
        swapped_361 = False
        for j_361 in range(n_361 - 1 - i_361):
            if a_361[j_361] > a_361[j_361 + 1]:
                a_361[j_361], a_361[j_361 + 1] = a_361[j_361 + 1], a_361[j_361]
                swapped_361 = True
        if not swapped_361:
            break
    return a_361

def merge_sort_361(arr_361):
    if len(arr_361) <= 1:
        return arr_361[:]
    mid_361 = len(arr_361) // 2
    left_361 = merge_sort_361(arr_361[:mid_361])
    right_361 = merge_sort_361(arr_361[mid_361:])
    return merge_361(left_361, right_361)

def merge_361(left_361, right_361):
    result_361 = []
    i_361 = j_361 = 0
    while i_361 < len(left_361) and j_361 < len(right_361):
        if left_361[i_361] <= right_361[j_361]:
            result_361.append(left_361[i_361]); i_361 += 1
        else:
            result_361.append(right_361[j_361]); j_361 += 1
    result_361.extend(left_361[i_361:])
    result_361.extend(right_361[j_361:])
    return result_361

INPUT_SIZES_361 = [100, 500, 1000, 2000, 4000, 8000]
TRIALS_361 = 5 

def benchmark_361(size_361):
    bubble_times_361 = []
    merge_times_361 = []
    for _ in range(TRIALS_361):
        data_361 = [random.randint(0, size_361 * 10) for _ in range(size_361)]

        start_361 = time.perf_counter()
        bubble_sort_361(data_361)
        bubble_times_361.append(time.perf_counter() - start_361)

        start_361 = time.perf_counter()
        merge_sort_361(data_361)
        merge_times_361.append(time.perf_counter() - start_361)

    return sum(bubble_times_361) / TRIALS_361, sum(merge_times_361) / TRIALS_361

def main_361():
    results_361 = []
    print(f"{'Size':>8} | {'Bubble (s)':>14} | {'Merge (s)':>14} | {'Speedup':>10}")
    print("-" * 55)
    for size_361 in INPUT_SIZES_361:
        bt_361, mt_361 = benchmark_361(size_361)
        speedup_361 = bt_361 / mt_361 if mt_361 > 0 else float('inf')
        results_361.append({'size': size_361, 'bubble_time_s': bt_361, 'merge_time_s': mt_361, 'speedup': speedup_361})
        print(f"{size_361:>8} | {bt_361:>14.6f} | {mt_361:>14.6f} | {speedup_361:>10.1f}x")

    with open('q2_results.csv', 'w', newline='') as f_361:
        writer_361 = csv.DictWriter(f_361, fieldnames=['size', 'bubble_time_s', 'merge_time_s', 'speedup'])
        writer_361.writeheader()
        writer_361.writerows(results_361)
    print("\nSaved results to q2_results.csv")

if __name__ == '__main__':
    main_361()