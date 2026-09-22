"""
Q2: Merge Sort Analysis (Menu-Driven Program)
"""

import random
import time
import matplotlib.pyplot as plt

array_361 = []          


# ---------- Merge Sort (counts comparisons) ----------
def merge_sort_361(arr_361, counter_361):
    """Sort arr_361 ascending using merge sort. counter_361[0] counts comparisons."""
    if len(arr_361) <= 1:
        return arr_361

    mid_361 = len(arr_361) // 2
    left_361 = merge_sort_361(arr_361[:mid_361], counter_361)
    right_361 = merge_sort_361(arr_361[mid_361:], counter_361)

    return merge_361(left_361, right_361, counter_361)


def merge_361(left_361, right_361, counter_361):
    result_361 = []
    i_361 = j_361 = 0

    while i_361 < len(left_361) and j_361 < len(right_361):
        counter_361[0] += 1                      
        if left_361[i_361] <= right_361[j_361]:
            result_361.append(left_361[i_361])
            i_361 += 1
        else:
            result_361.append(right_361[j_361])
            j_361 += 1

    result_361.extend(left_361[i_361:])
    result_361.extend(right_361[j_361:])
    return result_361


# ---------- Bubble Sort for descending order (counts comparisons) ----------
def bubble_sort_descending_361(arr_361):
    n_361 = len(arr_361)
    steps_361 = 0
    for i_361 in range(n_361 - 1):
        for j_361 in range(n_361 - 1 - i_361):
            steps_361 += 1
            if arr_361[j_361] < arr_361[j_361 + 1]:      # swap to get descending order
                arr_361[j_361], arr_361[j_361 + 1] = arr_361[j_361 + 1], arr_361[j_361]
    return arr_361, steps_361


# ---------- Menu option 1 ----------
def generate_array_361():
    global array_361
    n_361 = int(input("How many random numbers do you want to generate? "))
    low_361 = int(input("Enter lower bound: "))
    high_361 = int(input("Enter upper bound: "))
    array_361 = [random.randint(low_361, high_361) for _ in range(n_361)]
    print(f"Generated array: {array_361}")


# ---------- Menu option 2 ----------
def display_array_361():
    if not array_361:
        print("Array is empty. Please generate it first (option 1).")
    else:
        print(f"Current array: {array_361}")


# ---------- Menu option 3 ----------
def sort_ascending_361():
    if not array_361:
        print("Array is empty. Please generate it first (option 1).")
        return
    counter_361 = [0]
    sorted_arr_361 = merge_sort_361(array_361[:], counter_361)
    print(f"Ascending sorted array: {sorted_arr_361}")
    print(f"Number of comparisons (steps): {counter_361[0]}")


# ---------- Menu option 4 ----------
def sort_descending_361():
    if not array_361:
        print("Array is empty. Please generate it first (option 1).")
        return
    sorted_arr_361, steps_361 = bubble_sort_descending_361(array_361[:])
    print(f"Descending sorted array: {sorted_arr_361}")
    print(f"Number of comparisons (steps): {steps_361}")


# ---------- Helper for time-complexity menu options (5, 6, 7) ----------
def time_complexity_test_361(data_type_361):
    """
    data_type_361 is one of: 'random', 'sorted', 'reverse'
    Times merge sort on increasing array sizes and plots a graph.
    """
    sizes_361 = [100, 500, 1000, 2000, 4000, 6000]
    times_361 = []
    steps_361_list = []

    for size_361 in sizes_361:
        if data_type_361 == 'random':
            test_arr_361 = [random.randint(1, 100000) for _ in range(size_361)]
        elif data_type_361 == 'sorted':
            test_arr_361 = list(range(size_361))
        else:  # reverse
            test_arr_361 = list(range(size_361, 0, -1))

        counter_361 = [0]
        start_361 = time.perf_counter()
        merge_sort_361(test_arr_361, counter_361)
        end_361 = time.perf_counter()

        times_361.append(end_361 - start_361)
        steps_361_list.append(counter_361[0])

        print(f"n={size_361:<6} time={end_361 - start_361:.6f}s   steps={counter_361[0]}")

    plt.figure(figsize=(9, 5))
    plt.plot(sizes_361, times_361, marker='o')
    plt.xlabel("Array size (n)")
    plt.ylabel("Time (seconds)")
    plt.title(f"Merge Sort Time Complexity - {data_type_361} data")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    filename_361 = f"merge_sort_time_{data_type_361}_361.png"
    plt.savefig(filename_361)
    print(f"Graph saved as {filename_361}")


# ---------- Main menu loop ----------
def main():
    while True:
        print("\n===== Q2: Merge Sort Menu =====")
        print("1. Generate n random numbers -> array")
        print("2. Display array")
        print("3. Sort ascending (Merge Sort)")
        print("4. Sort descending (Bubble Sort)")
        print("5. Time complexity - ascending random data")
        print("6. Time complexity - ascending already-sorted data")
        print("7. Time complexity - ascending descending-sorted data")
        print("0. Exit")

        choice_361 = input("Enter your choice: ").strip()

        if choice_361 == '1':
            generate_array_361()
        elif choice_361 == '2':
            display_array_361()
        elif choice_361 == '3':
            sort_ascending_361()
        elif choice_361 == '4':
            sort_descending_361()
        elif choice_361 == '5':
            time_complexity_test_361('random')
        elif choice_361 == '6':
            time_complexity_test_361('sorted')
        elif choice_361 == '7':
            time_complexity_test_361('reverse')
        elif choice_361 == '0':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()