"""Pytest tests for closest.py."""

import math
import random

import pytest

from closest import closest_pair, closest_pair_brute


def check_answer(points, answer, expected_distance):
    """Check distance, index order, and the actual input pair."""
    distance, first, second = answer
    assert first < second
    actual = math.dist(points[first], points[second])
    assert math.isclose(distance, expected_distance, rel_tol=1e-12, abs_tol=1e-12)
    assert math.isclose(distance, actual, rel_tol=1e-12, abs_tol=1e-12)


def test_two_points():
    points = [(0, 0), (3, 4)]
    assert closest_pair(points) == (5.0, 0, 1)


def test_duplicate_points():
    points = [(1, 2), (9, 9), (1, 2), (4, 5)]
    answer = closest_pair(points)
    check_answer(points, answer, 0.0)


def test_vertical_line():
    points = [(7, 0), (7, 10), (7, 3), (7, 4)]
    answer = closest_pair(points)
    check_answer(points, answer, 1.0)


def test_pair_crosses_dividing_line():
    points = [(-10, 0), (10, 0), (-1, 1), (1, 1)]
    # Sorting by x puts the two closest points on opposite sides.
    sorted_points = sorted(points, key=lambda point: (point[0], point[1]))
    middle = len(sorted_points) // 2
    assert sorted_points[middle - 1][0] < 0 < sorted_points[middle][0]
    answer = closest_pair(points)
    assert {answer[1], answer[2]} == {2, 3}
    check_answer(points, answer, 2.0)


@pytest.mark.parametrize("case_number", range(500))
def test_random_lists(case_number):
    # A different deterministic seed is used for every test case.
    rng = random.Random(20261103 + case_number)
    count = rng.randint(2, 50)
    # Small integers create ties and duplicate coordinates.
    if case_number % 2 == 0:
        points = [(rng.randint(-10, 10), rng.randint(-10, 10)) for _ in range(count)]
    # Floats test the same algorithm with non-integer coordinates.
    else:
        points = [(rng.uniform(-100, 100), rng.uniform(-100, 100)) for _ in range(count)]
    expected = closest_pair_brute(points)
    actual = closest_pair(points)
    check_answer(points, actual, expected[0])
