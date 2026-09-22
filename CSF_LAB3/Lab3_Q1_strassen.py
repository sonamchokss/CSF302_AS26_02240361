"""
Q1 (part 2): Strassen's Matrix Multiplication vs Traditional
"""

import time
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from Lab3_Q1_matrix_mult import generate_matrix, traditional_multiply, matrices_equal


# ---------- Basic matrix helpers (needed for the divide & conquer steps) ----------

def add_matrix(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def sub_matrix(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def split_matrix(M):
    """Split an n x n matrix into four (n/2) x (n/2) quadrants."""
    n = len(M)
    mid = n // 2
    A11 = [row[:mid] for row in M[:mid]]
    A12 = [row[mid:] for row in M[:mid]]
    A21 = [row[:mid] for row in M[mid:]]
    A22 = [row[mid:] for row in M[mid:]]
    return A11, A12, A21, A22


def join_matrix(C11, C12, C21, C22):
    """Combine four quadrants back into a single matrix."""
    top = [r1 + r2 for r1, r2 in zip(C11, C12)]
    bottom = [r1 + r2 for r1, r2 in zip(C21, C22)]
    return top + bottom


# ---------- Strassen's algorithm ----------

def strassen_multiply(A, B):

    n = len(A)

    if n == 1:
        return [[A[0][0] * B[0][0]]]

    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)

    M1 = strassen_multiply(add_matrix(A11, A22), add_matrix(B11, B22))
    M2 = strassen_multiply(add_matrix(A21, A22), B11)
    M3 = strassen_multiply(A11, sub_matrix(B12, B22))
    M4 = strassen_multiply(A22, sub_matrix(B21, B11))
    M5 = strassen_multiply(add_matrix(A11, A12), B22)
    M6 = strassen_multiply(sub_matrix(A21, A11), add_matrix(B11, B12))
    M7 = strassen_multiply(sub_matrix(A12, A22), add_matrix(B21, B22))

    C11 = add_matrix(sub_matrix(add_matrix(M1, M4), M5), M7)
    C12 = add_matrix(M3, M5)
    C21 = add_matrix(M2, M4)
    C22 = add_matrix(sub_matrix(add_matrix(M1, M3), M2), M6)

    return join_matrix(C11, C12, C21, C22)


def next_power_of_2(n):
    p = 1
    while p < n:
        p *= 2
    return p


def pad_matrix(M, size):
    n = len(M)
    if n == size:
        return M
    padded = [[0] * size for _ in range(size)]
    for i in range(n):
        for j in range(n):
            padded[i][j] = M[i][j]
    return padded


def unpad_matrix(M, size):
    return [row[:size] for row in M[:size]]


def strassen_multiply_any_size(A, B):
    n = len(A)
    size = next_power_of_2(n)
    A_pad = pad_matrix(A, size)
    B_pad = pad_matrix(B, size)
    C_pad = strassen_multiply(A_pad, B_pad)
    return unpad_matrix(C_pad, n)


# ---------- Experiment: correctness + timing comparison ----------

def run_comparison(sizes=(2, 4, 8, 16, 32, 64, 128), trials=1, seed=42):
    random.seed(seed)
    results = []
    print(f"{'n':>5} | {'Traditional (s)':>16} | {'Strassen (s)':>13} | {'Match?':>7}")
    print("-" * 52)

    for n in sizes:
        trad_times, strass_times = [], []
        match = True
        for _ in range(trials):
            A = generate_matrix(n)
            B = generate_matrix(n)

            t0 = time.perf_counter()
            C_trad = traditional_multiply(A, B)
            t1 = time.perf_counter()
            trad_times.append(t1 - t0)

            t0 = time.perf_counter()
            C_strass = strassen_multiply(A, B)  # n is already a power of 2 here
            t1 = time.perf_counter()
            strass_times.append(t1 - t0)

            if not matrices_equal(C_trad, C_strass):
                match = False

        avg_trad = sum(trad_times) / trials
        avg_strass = sum(strass_times) / trials
        results.append((n, avg_trad, avg_strass, match))
        print(f"{n:>5} | {avg_trad:16.6f} | {avg_strass:13.6f} | {str(match):>7}")

    return results


def plot_results(results, filename="matrix_time_comparison.png"):
    ns = [r[0] for r in results]
    trad = [r[1] for r in results]
    strass = [r[2] for r in results]

    plt.figure(figsize=(8, 5.5))
    plt.plot(ns, trad, marker='o', label='Traditional O(n^3)')
    plt.plot(ns, strass, marker='s', label="Strassen O(n^2.807)")
    plt.xlabel("Matrix size (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Matrix Multiplication: Traditional vs Strassen's Algorithm")
    plt.xscale('log', base=2)
    plt.yscale('log')
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"\nGraph saved as {filename}")


if __name__ == "__main__":
    n = 4
    A = generate_matrix(n)
    B = generate_matrix(n)
    print("Matrix A:", A)
    print("Matrix B:", B)
    C1 = traditional_multiply(A, B)
    C2 = strassen_multiply_any_size(A, B)
    print("Traditional result:", C1)
    print("Strassen result:   ", C2)
    print("Results match:", matrices_equal(C1, C2))

    # Full experiment: sizes 2 up to 128, timing comparison + graph
    print("\n=== Timing comparison: Traditional vs Strassen ===")
    results = run_comparison(sizes=(2, 4, 8, 16, 32, 64, 128))
    plot_results(results)
