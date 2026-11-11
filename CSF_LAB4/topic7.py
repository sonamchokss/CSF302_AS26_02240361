import random
import time


def time_it(func, *args):
    start = time.perf_counter()
    func(*args)
    return time.perf_counter() - start

def validate_matrix(A, n, m):
    if m <= 0:
        raise ValueError("Modulus m must be positive.")
    if n < 0:
        raise ValueError("Exponent n must not be negative.")
    size = len(A)
    if size == 0 or any(len(row) != size for row in A):
        raise ValueError("Matrix must be square.")


# ---- 7.1  Multiply two square matrices, reduce each element mod m ----
def mat_mul(A, B, m):
    size = len(A)
    C = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            total = 0
            for k in range(size):
                total += A[i][k] * B[k][j]
            C[i][j] = total % m
    return C


# ---- 7.2  Identity matrix (1s on the diagonal, 0s elsewhere) ---------
def identity(size):
    return [[1 if i == j else 0 for j in range(size)] for i in range(size)]


# ---- 7.3  Naive: multiply A by itself n times ------------------------
def mat_pow_naive(A, n, m):
    validate_matrix(A, n, m)
    size = len(A)
    base = [[x % m for x in row] for row in A]
    result = [[x % m for x in row] for row in identity(size)]
    for _ in range(n):
        result = mat_mul(result, base, m)
    return result


# ---- 7.4  Binary: repeated squaring ----------------------------------
def mat_pow_binary(A, n, m):
    validate_matrix(A, n, m)
    size = len(A)
    base = [[x % m for x in row] for row in A]
    result = [[x % m for x in row] for row in identity(size)]
    while n > 0:
        if n & 1:
            result = mat_mul(result, base, m)
        base = mat_mul(base, base, m)
        n >>= 1
    return result


# ---- 7.5  Compare naive vs binary ------------------------------------
def compare_mat_pow():
    print("\n=== Topic 7.5: naive vs binary matrix power ===")
    tests = [
        ([[1, 1], [1, 0]], 10, 1000),
        ([[2, 3], [4, 5]], 20, 97),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 15, 1000),
        ([[2, 0], [0, 2]], 0, 13),       # n = 0 -> identity matrix
    ]
    for A, n, m in tests:
        r1 = mat_pow_naive(A, n, m)
        r2 = mat_pow_binary(A, n, m)
        print(f"A={A}, n={n}, m={m}")
        print(f"   naive : {r1}")
        print(f"   binary: {r2}")
        print(f"   match : {r1 == r2}")


# ---- 7.6  Fibonacci mod m using matrix power -------------------------
# [[1,1],[1,0]]^n = [[F(n+1), F(n)], [F(n), F(n-1)]]
def fib_mod(n, m):
    if n < 0:
        raise ValueError("n must not be negative.")
    if m <= 0:
        raise ValueError("m must be positive.")
    if n == 0:
        return 0 % m
    M = mat_pow_binary([[1, 1], [1, 0]], n, m)
    return M[0][1]                  # this entry is F(n) mod m


# ---- 7.7  Large Fibonacci without generating earlier ones ------------
def large_fibonacci_demo():
    print("\n=== Topic 7.6 / 7.7: Fibonacci with matrix power ===")
    print("First 10 Fibonacci numbers:", [fib_mod(i, 10**9) for i in range(10)])
    m = 10**9 + 7
    for n in [50, 1000, 10**6, 10**12, 10**18]:
        print(f"F({n}) mod {m} = {fib_mod(n, m)}")


# ---- 7.8  Count walks of exactly k edges in a directed graph ---------
def count_walks(adj, u, v, k, m):
    """adj[i][j] = 1 if there is an edge i -> j.
    (adj^k)[u][v] = number of walks with exactly k edges from u to v."""
    P = mat_pow_binary(adj, k, m)
    return P[u][v]


def walks_demo():
    print("\n=== Topic 7.8: walks in a directed graph ===")
    # Edges: 0->1, 0->2, 1->2, 2->0, 2->3, 3->1
    adj = [
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 0, 0],
    ]
    m = 10**9 + 7
    for (u, v, k) in [(0, 2, 1), (0, 2, 2), (0, 3, 3), (0, 0, 10), (0, 3, 1000)]:
        print(f"walks of exactly {k} edges from {u} to {v}: {count_walks(adj, u, v, k, m)}")


# ---- 7.9  Benchmark naive vs binary matrix power ---------------------
def random_matrix(size, m):
    return [[random.randint(0, m - 1) for _ in range(size)] for _ in range(size)]


def benchmark_mat_pow():
    print("\n=== Topic 7.9: matrix benchmark (m = 1000000007) ===")
    m = 10**9 + 7
    print(f"{'dim':>4} {'n':>8} | {'naive (s)':>12} | {'binary (s)':>12}")
    for size in [2, 5, 10]:
        A = random_matrix(size, m)
        for n in [10, 100, 1000, 3000]:
            t1 = time_it(mat_pow_naive, A, n, m)
            t2 = time_it(mat_pow_binary, A, n, m)
            print(f"{size:>4} {n:>8} | {t1:>12.6f} | {t2:>12.6f}")


# =====================================================================
if __name__ == "__main__":
    compare_mat_pow()
    large_fibonacci_demo()
    walks_demo()
    benchmark_mat_pow()
