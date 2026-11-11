import time


# =====================================================================
# TOPIC 6: MODULAR EXPONENTIATION   (compute a^b mod m)
# =====================================================================

# ---- 6.5  Input validation ------------------------------------------
def validate(a, b, m):
    if m <= 0:
        raise ValueError("Modulus m must be a positive integer (m > 0).")
    if b < 0:
        raise ValueError("Exponent b must not be negative.")
    # Zero exponent is fine: a^0 = 1  (handled by result = 1 % m below)
    # Negative base is fine: a % m turns it into a number between 0 and m-1


# ---- 6.1  Naive: multiply a by itself b times ------------------------
def naive_mod_pow(a, b, m):
    validate(a, b, m)
    a = a % m
    result = 1 % m              # 1 % m so that m = 1 gives 0
    for _ in range(b):          # b multiplications  -> O(b)
        result = (result * a) % m
    return result


# ---- 6.2  Binary exponentiation (square and multiply) ----------------
def binary_mod_pow_basic(a, b, m):
    validate(a, b, m)
    a = a % m
    result = 1 % m
    while b > 0:
        if b % 2 == 1:              # exponent is odd
            result = (result * a) % m
        a = (a * a) % m             # square the base
        b = b // 2                  # halve the exponent
    return result


# ---- 6.4  Same thing, but with bitwise operations --------------------
def binary_mod_pow(a, b, m):
    validate(a, b, m)
    a = a % m
    result = 1 % m
    while b > 0:
        if b & 1:                   # (b & 1) is 1 when b is odd
            result = (result * a) % m
        a = (a * a) % m
        b >>= 1                     # b >>= 1 is the same as b //= 2
    return result                   # only about log2(b) steps -> O(log b)


# ---- 6.3  Compare naive vs binary on different inputs ----------------
def compare_mod_pow():
    print("=== Topic 6.3: naive vs binary (vs Python's pow) ===")
    tests = [
        (2, 10, 1000),
        (3, 200, 13),
        (7, 0, 11),          # zero exponent
        (-5, 3, 7),          # negative base
        (10, 500, 1),        # m = 1
        (123456789, 1000, 1000000007),
        (2, 5000, 99991),
    ]
    print(f"{'a':>10} {'b':>6} {'m':>12} | {'naive':>10} {'binary':>10} {'pow()':>10} | match")
    for a, b, m in tests:
        n = naive_mod_pow(a, b, m)
        bi = binary_mod_pow(a, b, m)
        py = pow(a, b, m)
        print(f"{a:>10} {b:>6} {m:>12} | {n:>10} {bi:>10} {py:>10} | {n == bi == py}")


def test_validation():
    print("\n=== Topic 6.5: input validation ===")
    for a, b, m in [(2, -3, 5), (2, 3, 0), (2, 3, -7), (2, 0, 5), (-2, 3, 5)]:
        try:
            print(f"a={a}, b={b}, m={m} -> {binary_mod_pow(a, b, m)}")
        except ValueError as e:
            print(f"a={a}, b={b}, m={m} -> Error: {e}")


# ---- 6.6  Timing -----------------------------------------------------
def time_it(func, *args):
    start = time.perf_counter()
    func(*args)
    return time.perf_counter() - start


def benchmark_mod_pow():
    print("\n=== Topic 6.6: timing (a=7, m=1000000007) ===")
    print(f"{'exponent':>10} | {'naive (s)':>12} | {'binary (s)':>12}")
    for b in [10**2, 10**3, 10**4, 10**5, 10**6]:
        t1 = time_it(naive_mod_pow, 7, b, 1000000007)
        t2 = time_it(binary_mod_pow, 7, b, 1000000007)
        print(f"{b:>10} | {t1:>12.6f} | {t2:>12.6f}")



# =====================================================================
if __name__ == "__main__":
    compare_mod_pow()
    test_validation()
    benchmark_mod_pow()
