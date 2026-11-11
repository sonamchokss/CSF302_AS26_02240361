# Lab 4 - Efficient Modular Exponentiation and Efficient Matrix Modular Exponentiation

---

## 1. Aim

To implement and compare naive and efficient (binary / repeated-squaring) methods for computing powers under a modulus, first for numbers (`a^b mod m`) and then for square matrices (`A^n mod m`), and to apply matrix exponentiation to practical problems such as large Fibonacci numbers and counting walks in a directed graph.

---

## 2. Objectives

**Topic 6: Efficient Modular Exponentiation**

1. Implement naive modular exponentiation using repeated multiplication.
2. Implement binary exponentiation using the square-and-multiply method.
3. Compare the outputs of both methods for different bases, exponents and moduli.
4. Use bitwise operations (`b & 1` and `b >>= 1`) in the binary method.
5. Add input validation for zero exponents, negative exponents, negative bases and invalid moduli.
6. Measure and compare execution times for increasing exponents.

**Topic 7: Efficient Matrix Modular Exponentiation**

1. Multiply two square matrices with each element reduced modulo `m`.
2. Generate an identity matrix of any size.
3. Implement naive matrix exponentiation.
4. Implement binary matrix exponentiation (repeated squaring).
5. Compare naive and binary matrix exponentiation.
6. Compute the nth Fibonacci number modulo `m` using matrix exponentiation.
7. Compute very large Fibonacci numbers without generating the earlier ones.
8. Count walks of exactly `k` edges between two vertices of a directed graph.
9. Benchmark naive and binary matrix exponentiation for different dimensions and exponents.

---

## 3. Procedure / Steps

### Topic 6: Modular Exponentiation (`topic6.py`)

**Step 1 — Naive method (`naive_mod_pow`).**
Start with `result = 1`. Multiply `result` by `a` exactly `b` times, and take `% m` after every multiplication so the numbers never become huge. This needs `b` multiplications, so the time is **O(b)**.

**Step 2 — Binary exponentiation (`binary_mod_pow_basic`).**
The exponent is written in binary, so `a^b` is built from `a`, `a²`, `a⁴`, `a⁸`, ... For example, 3¹³ = 3⁸ × 3⁴ × 3¹ because 13 = `1101` in binary. In each loop:
- if `b` is odd, multiply `result` by the current `a`;
- square `a` (`a = a * a % m`);
- halve `b`.

This needs only about log₂(b) loops, so the time is **O(log b)**.

**Step 3 — Comparison program (`compare_mod_pow`).**
Run naive, binary and Python's built-in `pow(a, b, m)` on several test cases and print whether all three answers match.

**Step 4 — Bitwise version (`binary_mod_pow`).**
Replace `b % 2 == 1` with `b & 1` (checks the last bit), and replace `b = b // 2` with `b >>= 1` (shifts bits right by one). The logic is the same, but the operations are lower-level.

**Step 5 — Input validation (`validate`).**
- `m <= 0` → raise an error (modulus must be positive).
- `b < 0` → raise an error (no negative exponents in integer modular arithmetic).
- `b = 0` → return `1 % m` (any number to the power 0 is 1).
- negative base → use `a % m` to convert it into the range `0` to `m-1`.
- `m = 1` → the answer is always 0.

**Step 6 — Timing (`benchmark_mod_pow`).**
Use `time.perf_counter()` to time both methods for exponents 10², 10³, 10⁴, 10⁵ and 10⁶.

### Topic 7: Matrix Modular Exponentiation (`topic7.py`)

**Step 1 — Matrix multiplication (`mat_mul`).**
For each position `(i, j)`, add up `A[i][k] * B[k][j]` over all `k`, then take `% m`. Cost: O(d³) for a d × d matrix.

**Step 2 — Identity matrix (`identity`).**
A d × d matrix with 1 on the diagonal and 0 everywhere else. It acts like the number 1: `A × I = A`.

**Step 3 — Naive matrix power (`mat_pow_naive`).**
Start with the identity matrix and multiply by `A` exactly `n` times. Cost: O(d³ · n).

**Step 4 — Binary matrix power (`mat_pow_binary`).**
Same square-and-multiply idea as Topic 6, but with matrices: if `n` is odd, multiply the result by the current matrix; then square the matrix and halve `n`. Cost: O(d³ · log n).

**Step 5 — Comparison (`compare_mat_pow`).**
Run both methods on several matrices (including `n = 0`) and check that the results are identical.

**Step 6 — Fibonacci with matrices (`fib_mod`).**
Use the matrix `[[1, 1], [1, 0]]`. Raised to the power `n`, it equals
`[[F(n+1), F(n)], [F(n), F(n-1)]]`, so the top-right element is `F(n) mod m`.

**Step 7 — Large Fibonacci numbers (`large_fibonacci_demo`).**
Call `fib_mod` for n = 50, 1000, 10⁶, 10¹² and 10¹⁸. No earlier Fibonacci numbers are generated; only about log₂(n) matrix multiplications are needed.

**Step 8 — Counting walks (`count_walks`).**
Build the adjacency matrix `adj` (`adj[i][j] = 1` if there is an edge `i → j`). The entry `(adj^k)[u][v]` is the number of walks of exactly `k` edges from `u` to `v`. The graph used had edges 0→1, 0→2, 1→2, 2→0, 2→3, 3→1.

**Step 9 — Benchmark (`benchmark_mat_pow`).**
Time naive and binary matrix power for dimensions 2, 5 and 10 and exponents 10, 100, 1000 and 3000, using random matrices.

---

## 4. Results

### Topic 6: Outputs match for all test cases

| a | b | m | Naive | Binary | `pow()` | Match |
|---:|---:|---:|---:|---:|---:|:---:|
| 2 | 10 | 1000 | 24 | 24 | 24 | True |
| 3 | 200 | 13 | 9 | 9 | 9 | True |
| 7 | 0 | 11 | 1 | 1 | 1 | True |
| -5 | 3 | 7 | 1 | 1 | 1 | True |
| 10 | 500 | 1 | 0 | 0 | 0 | True |
| 123456789 | 1000 | 1000000007 | 620139939 | 620139939 | 620139939 | True |
| 2 | 5000 | 99991 | 78673 | 78673 | 78673 | True |

**Validation results**

| Input (a, b, m) | Output |
|---|---|
| (2, -3, 5) | Error: exponent must not be negative |
| (2, 3, 0) | Error: modulus must be positive |
| (2, 3, -7) | Error: modulus must be positive |
| (2, 0, 5) | 1 |
| (-2, 3, 5) | 2 |

**Timing (a = 7, m = 1000000007)**

| Exponent | Naive (s) | Binary (s) |
|---:|---:|---:|
| 100 | 0.000061 | 0.000012 |
| 1,000 | 0.000096 | 0.000005 |
| 10,000 | 0.000828 | 0.000006 |
| 100,000 | 0.010490 | 0.000010 |
| 1,000,000 | 0.058634 | 0.000006 |

### Topic 7

**Naive vs binary matrix power** — results were identical in all four test cases, for example:

- `[[1,1],[1,0]]^10 mod 1000 = [[89, 55], [55, 34]]`
- `[[2,3],[4,5]]^20 mod 97 = [[20, 11], [47, 31]]`
- `[[2,0],[0,2]]^0 mod 13 =` identity matrix `[[1,0],[0,1]]`

**Fibonacci using matrix exponentiation**

- First ten values: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34 (correct).

| n | F(n) mod 1000000007 |
|---:|---:|
| 50 | 586268941 |
| 1,000 | 517691607 |
| 1,000,000 | 918091266 |
| 10¹² | 730695249 |
| 10¹⁸ | 209783453 |

**Walks in the directed graph (mod 1000000007)**

| From → To | Edges (k) | Number of walks |
|---|---:|---:|
| 0 → 2 | 1 | 1 |
| 0 → 2 | 2 | 1 |
| 0 → 3 | 3 | 1 |
| 0 → 0 | 10 | 19 |
| 0 → 3 | 1000 | 396304088 |

**Matrix benchmark (m = 1000000007)**

| Dimension | n | Naive (s) | Binary (s) |
|---:|---:|---:|---:|
| 2 | 10 | 0.000034 | 0.000015 |
| 2 | 100 | 0.000177 | 0.000021 |
| 2 | 1000 | 0.001548 | 0.000029 |
| 2 | 3000 | 0.004503 | 0.000033 |
| 5 | 10 | 0.000364 | 0.000067 |
| 5 | 100 | 0.002427 | 0.000162 |
| 5 | 1000 | 0.014211 | 0.000188 |
| 5 | 3000 | 0.033932 | 0.000213 |
| 10 | 10 | 0.000697 | 0.000452 |
| 10 | 100 | 0.006199 | 0.000618 |
| 10 | 1000 | 0.066040 | 0.001090 |
| 10 | 3000 | 0.198230 | 0.00117 |

---

## Conclusion

- Naive and binary modular exponentiation gave the same answers in all tests and matched Python's `pow()`, so the binary method is correct.
- Naive takes O(b) time, while binary takes O(log b). For exponent 1,000,000, naive took 0.058635 s but binary took about 0.000006 s, roughly 10,000 times faster.
- The same idea works for matrices. For a 10 × 10 matrix with n = 3000, naive took 0.198230 s and binary took 0.001117 s, about 177 times faster.
- Matrix exponentiation computed F(10¹⁸) mod 1000000007 = 209783453 almost instantly and correctly counted walks of exactly k edges in a directed graph.
- Input validation handled zero and negative exponents, negative bases and invalid moduli.

## Reflection

I learned that exponentiation by squaring is much faster than repeated multiplication, because it uses binary representation of the exponent. It was surprising to learn that the same approach works for matrices. The most challenging part was to understand why Fibonacci matrix returns F(n) in the top right corner and how to handle the edge cases like m = 1 and b = 0. What I would do differently is to test the timing multiple times and take an average value and write more automated tests. Such methods find their applications in cryptography (RSA algorithm), computation of Fibonacci numbers and solution of graph problems.