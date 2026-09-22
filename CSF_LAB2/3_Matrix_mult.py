"""
Q3: Square Matrix Multiplication
"""

import random


# ---------- Create a matrix manually ----------
def input_matrix_manual_361(n_361, name_361):
    print(f"\nEnter matrix {name_361} row by row ({n_361} numbers per row, space separated):")
    matrix_361 = []
    for row_361 in range(n_361):
        while True:
            values_361 = input(f"Row {row_361 + 1}: ").split()
            if len(values_361) == n_361:
                matrix_361.append([int(v_361) for v_361 in values_361])
                break
            print(f"Please enter exactly {n_361} numbers.")
    return matrix_361


# ---------- Create a matrix randomly ----------
def input_matrix_random_361(n_361):
    return [[random.randint(1, 20) for _ in range(n_361)] for _ in range(n_361)]


# ---------- Display a matrix nicely ----------
def display_matrix_361(matrix_361, name_361):
    print(f"\nMatrix {name_361}:")
    for row_361 in matrix_361:
        print(row_361)


# ---------- Multiply two square matrices (naive method) ----------
def multiply_matrices_361(a_361, b_361):
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


# ---------- Check that n is a power of 2 ----------
def is_power_of_2_361(n_361):
    return n_361 > 0 and (n_361 & (n_361 - 1)) == 0


# ---------- Main Program ----------
def main():
    print("=== Q3: Square Matrix Multiplication ===")

    while True:
        n_361 = int(input("Enter size of the square matrix (must be a power of 2, e.g. 2, 4, 8, 16): "))
        if is_power_of_2_361(n_361):
            break
        print("That is not a power of 2. Try again.")

    mode_361 = input("Type 'm' to enter matrices manually, or 'r' for random values: ").strip().lower()

    if mode_361 == 'm':
        matrix_a_361 = input_matrix_manual_361(n_361, "A")
        matrix_b_361 = input_matrix_manual_361(n_361, "B")
    else:
        matrix_a_361 = input_matrix_random_361(n_361)
        matrix_b_361 = input_matrix_random_361(n_361)

    display_matrix_361(matrix_a_361, "A")
    display_matrix_361(matrix_b_361, "B")

    result_361, operations_361 = multiply_matrices_361(matrix_a_361, matrix_b_361)

    display_matrix_361(result_361, "Result (A x B)")
    print(f"\nTotal basic operations (multiplications + additions): {operations_361}")
    print(f"Expected by formula 2*n^3 = {2 * n_361 ** 3}")

if __name__ == "__main__":
    main()