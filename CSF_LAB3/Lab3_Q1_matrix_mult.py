"""
Q1 (part 1): Traditional Matrix Multiplication
"""

import random


def generate_matrix(n, low=0, high=9):
    return [[random.randint(low, high) for _ in range(n)] for _ in range(n)]


def traditional_multiply(A, B):
    n = len(A)
    m = len(B[0])
    p = len(B)
    C = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            total = 0
            for k in range(p):
                total += A[i][k] * B[k][j]
            C[i][j] = total
    return C


def print_matrix(M, name="Matrix"):
    print(f"\n{name}:")
    for row in M:
        print(row)


def matrices_equal(A, B):
    return A == B


if __name__ == "__main__":
    # Simple manual demo when this file is run directly
    n = 4
    A = generate_matrix(n)
    B = generate_matrix(n)

    print_matrix(A, "Matrix A")
    print_matrix(B, "Matrix B")

    C = traditional_multiply(A, B)
    print_matrix(C, "A x B (Traditional)")
