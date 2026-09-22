"""
Q3: Strassen's Matrix Multiplication vs Naive Method
"""

import random
import time
import matplotlib.pyplot as plt


# ---------- Naive multiplication (for comparison) ----------
def naive_multiply_361(a_361, b_361):
    n_361 = len(a_361)
    result_361 = [[0] * n_361 for _ in range(n_361)]
    operations_361 = 0
    for i_361 in range(n_361):
        for j_361 in range(n_361):
            total_361 = 0
            for k_361 in range(n_361):
                total_361 += a_361[i_361][k_361] * b_361[k_361][j_361]
                operations_361 += 2
            result_361[i_361][j_361] = total_361
    return result_361, operations_361


# ---------- Matrix helper functions ----------
def add_matrix_361(a_361, b_361):
    return [[a_361[i][j] + b_361[i][j] for j in range(len(a_361))] for i in range(len(a_361))]


def sub_matrix_361(a_361, b_361):
    return [[a_361[i][j] - b_361[i][j] for j in range(len(a_361))] for i in range(len(a_361))]


def split_matrix_361(m_361):
    n_361 = len(m_361)
    mid_361 = n_361 // 2
    a11_361 = [row[:mid_361] for row in m_361[:mid_361]]
    a12_361 = [row[mid_361:] for row in m_361[:mid_361]]
    a21_361 = [row[:mid_361] for row in m_361[mid_361:]]
    a22_361 = [row[mid_361:] for row in m_361[mid_361:]]
    return a11_361, a12_361, a21_361, a22_361


def combine_matrix_361(c11_361, c12_361, c21_361, c22_361):
    top_361 = [c11_361[i] + c12_361[i] for i in range(len(c11_361))]
    bottom_361 = [c21_361[i] + c22_361[i] for i in range(len(c21_361))]
    return top_361 + bottom_361


# ---------- Strassen's algorithm (counts multiplications) ----------
def strassen_multiply_361(a_361, b_361, counter_361):
    n_361 = len(a_361)

    if n_361 == 1:
        counter_361[0] += 1
        return [[a_361[0][0] * b_361[0][0]]]

    a11_361, a12_361, a21_361, a22_361 = split_matrix_361(a_361)
    b11_361, b12_361, b21_361, b22_361 = split_matrix_361(b_361)

    # 7 recursive multiplications (this is the key trick of Strassen)
    m1_361 = strassen_multiply_361(add_matrix_361(a11_361, a22_361), add_matrix_361(b11_361, b22_361), counter_361)
    m2_361 = strassen_multiply_361(add_matrix_361(a21_361, a22_361), b11_361, counter_361)
    m3_361 = strassen_multiply_361(a11_361, sub_matrix_361(b12_361, b22_361), counter_361)
    m4_361 = strassen_multiply_361(a22_361, sub_matrix_361(b21_361, b11_361), counter_361)
    m5_361 = strassen_multiply_361(add_matrix_361(a11_361, a12_361), b22_361, counter_361)
    m6_361 = strassen_multiply_361(sub_matrix_361(a21_361, a11_361), add_matrix_361(b11_361, b12_361), counter_361)
    m7_361 = strassen_multiply_361(sub_matrix_361(a12_361, a22_361), add_matrix_361(b21_361, b22_361), counter_361)

    c11_361 = add_matrix_361(sub_matrix_361(add_matrix_361(m1_361, m4_361), m5_361), m7_361)
    c12_361 = add_matrix_361(m3_361, m5_361)
    c21_361 = add_matrix_361(m2_361, m4_361)
    c22_361 = add_matrix_361(sub_matrix_361(add_matrix_361(m1_361, m3_361), m2_361), m6_361)

    return combine_matrix_361(c11_361, c12_361, c21_361, c22_361)


# ---------- Main: compare naive vs strassen ----------
def main():
    print("=== Q3 Bonus: Naive vs Strassen Matrix Multiplication ===")

    sizes_361 = [2, 4, 8, 16, 32, 64]     
    naive_times_361 = []
    strassen_times_361 = []

    print("\n{:<8}{:<18}{:<18}".format("Size", "Naive Time (s)", "Strassen Time (s)"))
    print("-" * 44)

    for n_361 in sizes_361:
        matrix_a_361 = [[random.randint(1, 10) for _ in range(n_361)] for _ in range(n_361)]
        matrix_b_361 = [[random.randint(1, 10) for _ in range(n_361)] for _ in range(n_361)]

        start_361 = time.perf_counter()
        naive_multiply_361(matrix_a_361, matrix_b_361)
        naive_time_361 = time.perf_counter() - start_361

        mult_counter_361 = [0]
        start_361 = time.perf_counter()
        strassen_multiply_361(matrix_a_361, matrix_b_361, mult_counter_361)
        strassen_time_361 = time.perf_counter() - start_361

        naive_times_361.append(naive_time_361)
        strassen_times_361.append(strassen_time_361)

        print("{:<8}{:<18.6f}{:<18.6f}".format(n_361, naive_time_361, strassen_time_361))

    plt.figure(figsize=(9, 5))
    plt.plot(sizes_361, naive_times_361, marker='o', label='Naive (O(n^3))')
    plt.plot(sizes_361, strassen_times_361, marker='s', label='Strassen (O(n^2.81))')
    plt.xlabel("Matrix size (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Naive vs Strassen Matrix Multiplication - Time Complexity")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("strassen_vs_naive_361.png")
    print("\nGraph saved as strassen_vs_naive_361.png")

if __name__ == "__main__":
    main()