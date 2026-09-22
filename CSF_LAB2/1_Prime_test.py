"""
Q1: Prime Number Testing
"""

import time
import matplotlib.pyplot as plt


# ---------- Algorithm 1: Naive Method ----------
def naive_prime_361(n_361):
    """Return (is_prime, steps) using naive division from 2 to n-1."""
    steps_361 = 0

    if n_361 < 2:
        return False, steps_361

    for i_361 in range(2, n_361):        
        steps_361 += 1                   
        if n_361 % i_361 == 0:
            return False, steps_361

    return True, steps_361


# ---------- Algorithm 2: Optimized Method ----------
def optimized_prime_361(n_361):
    """Return (is_prime, steps) using division only up to sqrt(n)."""
    steps_361 = 0

    if n_361 < 2:
        return False, steps_361

    i_361 = 2
    while i_361 * i_361 <= n_361:        
        steps_361 += 1
        if n_361 % i_361 == 0:
            return False, steps_361
        i_361 += 1

    return True, steps_361


# ---------- Algorithm 3 (Optional): Sieve of Eratosthenes ----------
def sieve_of_eratosthenes_361(limit_361):
    """Return list of all primes from 2 up to limit_361 (inclusive)."""
    is_prime_361 = [True] * (limit_361 + 1)
    is_prime_361[0] = False
    if limit_361 >= 1:
        is_prime_361[1] = False

    for i_361 in range(2, int(limit_361 ** 0.5) + 1):
        if is_prime_361[i_361]:
            for j_361 in range(i_361 * i_361, limit_361 + 1, i_361):
                is_prime_361[j_361] = False

    primes_361 = [num for num, flag in enumerate(is_prime_361) if flag]
    return primes_361


# ---------- Main Program ----------
def main():
    print("=== Q1: Prime Number Testing ===")
    print("Enter at least 10 numbers (one at a time). Type 'done' after 10 to stop early won't work - just enter 10.\n")

    numbers_361 = []
    count_needed_361 = 10
    while len(numbers_361) < count_needed_361:
        raw_361 = input(f"Enter number {len(numbers_361) + 1}: ")
        try:
            numbers_361.append(int(raw_361))
        except ValueError:
            print("Please enter a valid integer.")

    # table headers
    print("\n{:<10}{:<12}{:<15}{:<12}{:<15}{:<10}".format(
        "Number", "Naive?", "Naive Steps", "Optim?", "Optim Steps", "Match?"))
    print("-" * 75)

    naive_steps_list_361 = []
    optimized_steps_list_361 = []

    for n_361 in numbers_361:
        naive_result_361, naive_steps_361 = naive_prime_361(n_361)
        optim_result_361, optim_steps_361 = optimized_prime_361(n_361)

        naive_steps_list_361.append(naive_steps_361)
        optimized_steps_list_361.append(optim_steps_361)

        match_361 = "Yes" if naive_result_361 == optim_result_361 else "NO!"

        print("{:<10}{:<12}{:<15}{:<12}{:<15}{:<10}".format(
            n_361, str(naive_result_361), naive_steps_361,
            str(optim_result_361), optim_steps_361, match_361))

    # Optional: Sieve of Eratosthenes demo
    print("\n--- Optional: Sieve of Eratosthenes ---")
    limit_361 = max(numbers_361) if numbers_361 else 50
    limit_361 = max(limit_361, 2)
    primes_found_361 = sieve_of_eratosthenes_361(limit_361)
    print(f"All primes from 2 to {limit_361}: {primes_found_361}")

    # ---------- Graph: step count comparison ----------
    x_positions_361 = list(range(1, len(numbers_361) + 1))

    plt.figure(figsize=(9, 5))
    plt.plot(x_positions_361, naive_steps_list_361, marker='o', label='Naive Method (O(n))')
    plt.plot(x_positions_361, optimized_steps_list_361, marker='s', label='Optimized Method (O(sqrt n))')
    plt.xticks(x_positions_361, numbers_361)
    plt.xlabel("Input Number (n)")
    plt.ylabel("Number of Steps (comparisons)")
    plt.title("Naive vs Optimized Prime Test - Step Count Comparison")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("prime_test_graph_361.png")
    print("\nGraph saved as prime_test_graph_361.png")

if __name__ == "__main__":
    main()