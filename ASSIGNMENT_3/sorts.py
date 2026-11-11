"""In-place quicksort implementations for Assignment 3."""

import random


def _lomuto_partition(a, low, high):
    """Partition a[low:high + 1] around its last element."""
    pivot = a[high]
    boundary = low
    for index in range(low, high):
        if a[index] <= pivot:
            a[boundary], a[index] = a[index], a[boundary]
            boundary += 1
    a[boundary], a[high] = a[high], a[boundary]
    return boundary


def quicksort_basic(a):
    """Sort a in place using Lomuto partitioning and plain recursion."""
    def sort_range(low, high):
        if low >= high:
            return
        pivot_index = _lomuto_partition(a, low, high)
        sort_range(low, pivot_index - 1)
        sort_range(pivot_index + 1, high)

    sort_range(0, len(a) - 1)


def _insertion_sort_range(a, low, high):
    """Sort the inclusive range a[low:high + 1] by insertion sort."""
    for index in range(low + 1, high + 1):
        value = a[index]
        position = index - 1
        while position >= low and a[position] > value:
            a[position + 1] = a[position]
            position -= 1
        a[position + 1] = value


def quicksort_improved(a, cutoff=16):
    """Sort a in place with random pivots, a cutoff, and bounded recursion.

    After partitioning, recurse on the smaller side and loop over the larger
    side. The recursive side has at most half the current elements, so the
    recursion depth is bounded by log2(n), even when partitions are uneven.
    """
    if cutoff < 1:
        raise ValueError("cutoff must be at least 1")
    _sort_range(a, 0, len(a) - 1, cutoff)


def _sort_range(a, low, high, cutoff):
    """Sort one range, recursing on its smaller partition."""
    while low < high:
        if high - low + 1 <= cutoff:
            _insertion_sort_range(a, low, high)
            return

        pivot_index = random.randint(low, high)
        a[pivot_index], a[high] = a[high], a[pivot_index]
        pivot_index = _lomuto_partition(a, low, high)

        left_size = pivot_index - low
        right_size = high - pivot_index
        if left_size < right_size:
            _sort_range(a, low, pivot_index - 1, cutoff)
            low = pivot_index + 1
        else:
            _sort_range(a, pivot_index + 1, high, cutoff)
            high = pivot_index - 1
