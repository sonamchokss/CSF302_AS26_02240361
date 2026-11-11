"""Tests for the hall-booking algorithms."""

import random

import pytest

from booking import (best_schedule, brute_force, greedy_earliest_finish,
                     greedy_highest_fee)


FUNCTIONS = [greedy_earliest_finish, greedy_highest_fee, best_schedule,
             brute_force]


def assert_valid_result(requests, result):
    total, chosen = result
    assert chosen == sorted(chosen)
    assert len(chosen) == len(set(chosen))
    assert all(0 <= index < len(requests) for index in chosen)
    ordered = sorted(chosen, key=lambda i: (requests[i][0], requests[i][1], i))
    assert all(requests[ordered[i]][1] <= requests[ordered[i + 1]][0]
               for i in range(len(ordered) - 1))
    assert total == sum(requests[index][2] for index in chosen)


def test_explicit_cases():
    cases = [
        [],
        [(4, 7, 10)],
        [(1, 10, 5), (2, 9, 6), (3, 8, 7)],
        [(1, 2, 5), (2, 3, 6), (3, 4, 7)],
        [(1, 3, 5), (4, 6, 6), (7, 9, 7)],
    ]
    for requests in cases:
        for function in FUNCTIONS:
            assert_valid_result(requests, function(requests))


def test_given_example():
    requests = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000),
                (12, 14, 2500), (16, 18, 2000)]
    assert greedy_earliest_finish(requests) == (7500, [0, 3, 4])
    assert best_schedule(requests) == (10000, [1, 4])


def test_random_inputs_against_brute_force():
    rng = random.Random(20261103)
    for _ in range(600):
        requests = []
        for _ in range(rng.randint(0, 10)):
            start = rng.randint(0, 8)
            finish = rng.randint(start, 10)
            requests.append((start, finish, rng.randint(1, 30)))

        optimum = best_schedule(requests)[0]
        assert optimum == brute_force(requests)[0]
        for function in FUNCTIONS:
            result = function(requests)
            assert_valid_result(requests, result)
            assert result[0] <= optimum


def test_equal_fees_earliest_finish_is_optimal():
    rng = random.Random(302)
    for _ in range(300):
        requests = []
        for _ in range(rng.randint(0, 10)):
            start = rng.randint(0, 8)
            requests.append((start, rng.randint(start, 10), 7))
        assert greedy_earliest_finish(requests)[0] == best_schedule(requests)[0]


# TODO: replace None with a hand-made counterexample and expected optimum.
EARLIEST_FINISH_COUNTEREXAMPLE = None
HIGHEST_FEE_COUNTEREXAMPLE = None


@pytest.mark.skipif(EARLIEST_FINISH_COUNTEREXAMPLE is None,
                    reason="Insert your own earliest-finish counterexample.")
def test_earliest_finish_counterexample():
    requests, expected_optimum = EARLIEST_FINISH_COUNTEREXAMPLE
    assert greedy_earliest_finish(requests)[0] < expected_optimum
    assert greedy_earliest_finish(requests)[0] < best_schedule(requests)[0]


@pytest.mark.skipif(HIGHEST_FEE_COUNTEREXAMPLE is None,
                    reason="Insert your own highest-fee counterexample.")
def test_highest_fee_counterexample():
    requests, expected_optimum = HIGHEST_FEE_COUNTEREXAMPLE
    assert greedy_highest_fee(requests)[0] < expected_optimum
    assert greedy_highest_fee(requests)[0] < best_schedule(requests)[0]

