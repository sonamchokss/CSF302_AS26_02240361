"""
Q3: Binary Search vs Ternary Search (Menu-Driven Program)
"""

import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------- Search algorithms (each returns (found_index_or_-1, comparisons)) ----------

def binary_search(arr, key):
    low, high = 0, len(arr) - 1
    comparisons = 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if arr[mid] == key:
            return mid, comparisons
        comparisons += 1
        if arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1
    return -1, comparisons


def ternary_search(arr, key):
    low, high = 0, len(arr) - 1
    comparisons = 0
    while low <= high:
        mid1 = low + (high - low) // 3
        mid2 = high - (high - low) // 3

        comparisons += 1
        if arr[mid1] == key:
            return mid1, comparisons

        comparisons += 1
        if arr[mid2] == key:
            return mid2, comparisons

        comparisons += 1
        if key < arr[mid1]:
            high = mid1 - 1
        else:
            comparisons += 1
            if key > arr[mid2]:
                low = mid2 + 1
            else:
                low = mid1 + 1
                high = mid2 - 1
    return -1, comparisons


# ---------- Helper functions ----------

def generate_sorted_array(n, low=0, high=1000):
    arr = sorted(random.randint(low, high) for _ in range(n))
    return arr


def best_case_key(arr, algo):
    n = len(arr)
    if algo == "binary":
        mid = (0 + n - 1) // 2
        return arr[mid]
    else:  # ternary: either mid1 or mid2 works; use mid1
        low, high = 0, n - 1
        mid1 = low + (high - low) // 3
        return arr[mid1]


def worst_case_key(arr):
    return (arr[-1] if arr else 0) + 1  # one more than the max element


# ---------- Menu actions ----------

def action_generate(state):
    n = int(input("Enter n (array size): "))
    state["array"] = generate_sorted_array(n)
    print(f"Generated a sorted array of {n} elements.")


def action_display(state):
    if "array" not in state:
        print("No array generated yet. Use option 1 first.")
        return
    print("Array:", state["array"])


def action_search(state, algo):
    if "array" not in state:
        print("No array generated yet. Use option 1 first.")
        return
    key = int(input("Enter key to search for: "))
    fn = binary_search if algo == "binary" else ternary_search
    idx, comps = fn(state["array"], key)
    if idx != -1:
        print(f"Key {key} FOUND at index {idx}. Comparisons: {comps}")
    else:
        print(f"Key {key} NOT FOUND. Comparisons: {comps}")


def action_best_case(state):
    if "array" not in state:
        print("No array generated yet. Use option 1 first.")
        return
    arr = state["array"]
    bkey_bin = best_case_key(arr, "binary")
    bkey_ter = best_case_key(arr, "ternary")
    _, c_bin = binary_search(arr, bkey_bin)
    _, c_ter = ternary_search(arr, bkey_ter)
    print(f"Best case Binary Search : key={bkey_bin}, comparisons={c_bin}")
    print(f"Best case Ternary Search: key={bkey_ter}, comparisons={c_ter}")


def action_worst_case(state):
    if "array" not in state:
        print("No array generated yet. Use option 1 first.")
        return
    arr = state["array"]
    wkey = worst_case_key(arr)
    _, c_bin = binary_search(arr, wkey)
    _, c_ter = ternary_search(arr, wkey)
    print(f"Worst case Binary Search : key={wkey} (absent), comparisons={c_bin}")
    print(f"Worst case Ternary Search: key={wkey} (absent), comparisons={c_ter}")


def action_comparison_table(state, sizes=(10, 100, 1000, 10000, 100000, 1000000),
                             save_plot=True):
    print(f"\n{'n':>9} | {'Binary (worst)':>15} | {'Ternary (worst)':>16}")
    print("-" * 48)
    ns, bin_counts, ter_counts = [], [], []
    for n in sizes:
        arr = generate_sorted_array(n)
        wkey = worst_case_key(arr)
        _, c_bin = binary_search(arr, wkey)
        _, c_ter = ternary_search(arr, wkey)
        print(f"{n:>9} | {c_bin:>15} | {c_ter:>16}")
        ns.append(n)
        bin_counts.append(c_bin)
        ter_counts.append(c_ter)

    if save_plot:
        plt.figure(figsize=(8, 5.5))
        plt.plot(ns, bin_counts, marker='o', label='Binary Search comparisons')
        plt.plot(ns, ter_counts, marker='s', label='Ternary Search comparisons')
        plt.xlabel("Array size (n)")
        plt.ylabel("Number of comparisons (worst case)")
        plt.title("Binary vs Ternary Search: Comparison Counts")
        plt.xscale('log')
        plt.legend()
        plt.grid(True, which="both", linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig("search_comparison.png", dpi=150)
        print("\nGraph saved as search_comparison.png")

    return ns, bin_counts, ter_counts


# ---------- Menu loop ----------

MENU = """
========== Binary Search vs Ternary Search ==========
1. Generate n sorted random numbers -> Array
2. Display Array
3. Search for a key using Binary Search
4. Search for a key using Ternary Search
5. Step/frequency count for BEST case
6. Step/frequency count for WORST case
7. Step/frequency count comparison table across increasing n
8. Exit
=======================================================
"""

def main():
    state = {}
    while True:
        print(MENU)
        choice = input("Enter choice (1-8): ").strip()
        if choice == "1":
            action_generate(state)
        elif choice == "2":
            action_display(state)
        elif choice == "3":
            action_search(state, "binary")
        elif choice == "4":
            action_search(state, "ternary")
        elif choice == "5":
            action_best_case(state)
        elif choice == "6":
            action_worst_case(state)
        elif choice == "7":
            action_comparison_table(state)
        elif choice == "8":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()