import random


def minmax_361(A, lo, hi, minmax_count_361):
    """Returns (min, max) of A[lo..hi] using MINMAX divide and conquer.
    minmax_count_361 is a 1-element list used as a mutable comparison counter."""

    # Base case: one element
    if hi - lo == 0:
        return A[lo], A[lo]

    # Base case: two elements -> exactly 1 comparison
    if hi - lo == 1:
        minmax_count_361[0] += 1
        if A[lo] < A[hi]:
            return A[lo], A[hi]
        else:
            return A[hi], A[lo]

    # Divide
    mid = (lo + hi) // 2
    min1, max1 = minmax_361(A, lo, mid, minmax_count_361)
    min2, max2 = minmax_361(A, mid + 1, hi, minmax_count_361)

    # Combine: exactly 2 comparisons
    minmax_count_361[0] += 2
    overall_min = min1 if min1 < min2 else min2
    overall_max = max1 if max1 > max2 else max2

    return overall_min, overall_max


def predicted_361(n):
    """Closed form C(n) = 3n/2 - 2"""
    return (3 * n) // 2 - 2


def two_scan_361(n):
    """Naive two-scan comparison count"""
    return 2 * n - 2


if __name__ == "__main__":
    print(f"{'n':>6} | {'Measured':>10} | {'Predicted (3n/2-2)':>20} | {'Two-scan (2n-2)':>16}")
    print("-" * 62)

    for n in [8, 64, 512, 4096]:
        A = [random.randint(0, 10**9) for _ in range(n)]
        counter = [0]
        result_min, result_max = minmax_361(A, 0, n - 1, counter)

        # sanity check against Python's built-ins
        assert result_min == min(A), "MINMAX min mismatch!"
        assert result_max == max(A), "MINMAX max mismatch!"

        measured = counter[0]
        pred = predicted_361(n)
        naive = two_scan_361(n)

        print(f"{n:>6} | {measured:>10} | {pred:>20} | {naive:>16}")