"""Tests for both in-place sorting implementations."""

import random

import pytest

from sorts import quicksort_basic, quicksort_improved


SORTERS = [
    pytest.param(quicksort_basic, None, id="basic"),
    pytest.param(quicksort_improved, 1, id="improved-cutoff-1"),
    pytest.param(quicksort_improved, 4, id="improved-cutoff-4"),
    pytest.param(quicksort_improved, 16, id="improved-cutoff-16"),
    pytest.param(quicksort_improved, 64, id="improved-cutoff-64"),
]


@pytest.mark.parametrize("sorter, cutoff", SORTERS)
def test_explicit_cases(sorter, cutoff):
    cases = [
        [],
        [7],
        [5, 5, 5, 5],
        list(range(20)),
        list(range(20, 0, -1)),
        [-8, -3, -10, -1],
        [-4, 3, 0, -2, 8, 1],
    ]
    for original in cases:
        values = original[:]
        identity = id(values)
        result = sorter(values) if cutoff is None else sorter(values, cutoff)
        assert result is None
        assert id(values) == identity
        assert values == sorted(original)


@pytest.mark.parametrize("case_number", range(600))
@pytest.mark.parametrize("sorter, cutoff", SORTERS)
def test_random_inputs(sorter, cutoff, case_number):
    rng = random.Random(20261103 + case_number)
    maximum_length = 40 if sorter is quicksort_basic else 200
    values = [rng.randint(-30, 30) for _ in range(rng.randint(0, maximum_length))]
    expected = sorted(values)
    identity = id(values)
    result = sorter(values) if cutoff is None else sorter(values, cutoff)
    assert result is None
    assert id(values) == identity
    assert values == expected

