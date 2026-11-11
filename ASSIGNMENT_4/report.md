# Assignment 4: Booking the Hall

## 1. AI-use statement

I used claude for code drafting, test
design, experiment structure, and report scaffolding. I checked the code
against `brute_force`, including seeded random tests and explicit cases. 

## 2. Approach

The input is a list of `(start, finish, fee)` requests. Two requests are
compatible when one finishes no later than the other starts, so
`finish == start` is allowed for back-to-back bookings. All returned indices
refer to the original input list and are sorted in ascending order.

`greedy_earliest_finish` attaches each original index, sorts by
`(finish, start, fee, original_index)`, and accepts a request if its start is
at least the finish of the last accepted request.

`greedy_highest_fee` sorts by `(-fee, finish, start, original_index)`. For
each candidate it checks compatibility with every request already accepted.
The interval test accepts the candidate when it is completely before or
completely after every accepted interval.

`best_schedule` sorts by finish time using the same deterministic key. For
request `j`, `p(j)` is the number of earlier requests finishing no later than
`start_j`, computed with `bisect_right(finishes, start_j, hi=j)`. Its
recurrence is
`OPT(j) = max(OPT(j-1), fee_j + OPT(p(j)))`. A backward walk reconstructs
the selected original indices by comparing the include and exclude values.

`brute_force` enumerates all subsets, checks compatibility, and retains the
greatest fee; it is intended only for small inputs.

## 3. Verified counterexamples

The checked random search used `random.Random(20261103)`. Each trial had
0--10 requests; starts were uniform integers from 0 through 8, finishes were
uniform integers from the selected start through 10, and fees were uniform
integers from 1 through 30. The following are supplementary verification
search results using the existing functions; the current `experiments.py`
itself prints only the supplied example and the ratio experiment.

### Counterexample 1: earliest finish

Requests, in original-index order:
`[(3, 8, 21), (8, 8, 11), (5, 8, 24), (5, 8, 29), (3, 6, 17), (1, 1, 3), (4, 5, 17)]`.

**Table 1. Earliest-finish counterexample revenues.**

| Method | Total fee | Chosen indices |
|---|---:|---|
| Earliest finish | 55 | [1, 2, 5, 6] |
| Dynamic programming optimum | 60 | [1, 3, 5, 6] |
| Brute force | 60 | [1, 3, 5, 6] |

The rule takes index 2 (fee 24) instead of index 3 (fee 29); both finish at
8. Earliest finish has no fee criterion to distinguish them.

### Counterexample 2: highest fee

Requests, in original-index order:
`[(7, 7, 26), (4, 9, 29), (8, 10, 18), (1, 4, 27), (7, 9, 10), (6, 10, 2), (1, 1, 24)]`.

**Table 2. Highest-fee counterexample revenues.**

| Method | Total fee | Chosen indices |
|---|---:|---|
| Highest fee | 80 | [1, 3, 6] |
| Dynamic programming optimum | 95 | [0, 2, 3, 6] |
| Brute force | 95 | [0, 2, 3, 6] |

The rule accepts index 1 (fee 29), occupying time 4--9. This prevents indices
0 and 2, whose combined fees are 44. A high individual fee does not account
for how much schedule space the request consumes.

The supplied example also confirms the requested behavior:
`greedy_earliest_finish` returns `(7500, [0, 3, 4])`, while both
`best_schedule` and `brute_force` return `(10000, [1, 4])`. On that example,
the highest-fee rule also returns `(10000, [1, 4])`, so it is not itself a
counterexample for that particular input.

## 4. Why the DP recurrence is correct

After sorting by finish time, consider an optimum drawn from the first `j`
requests. If request `j` is not selected, the best value is `OPT(j-1)`.

If request `j` is selected, every other selected request must finish no later
than `start_j`, so the value is
`fee_j + OPT(p(j))`.

The remaining part must be optimal: otherwise a better schedule for the first
`p(j)` requests could replace it, a cut-and-paste contradiction. Therefore
the larger case is optimal:
`OPT(j) = max(OPT(j-1), fee_j + OPT(p(j)))`. The reconstruction code applies
the same comparison backwards, adding request `j` only when the include case
strictly improves the stored value.

## 5. Revenue-ratio experiment

The unchanged `experiments.py` ran 1,000 trials for each generator, with 50
requests per trial and seed `20261103`. For the `standard` generator,
`start` was uniform in `[0, 100]`, duration in `[1, 20]`, and fee in
`[100, 1000]`. For `short_durations`, the start and fee ranges were the same
but duration was in `[1, 5]`. Every trial's results were written to
`booking_ratios.csv`. The ratio is greedy revenue divided by the DP optimum.

**Table 3. Measured revenue ratios over 1,000 trials per generator.**

| Generator | Rule | Average ratio | Worst ratio |
|---|---|---:|---:|
| standard | earliest finish | 0.8375 | 0.5247 |
| standard | highest fee | 0.8643 | 0.4642 |
| short durations | earliest finish | 0.8557 | 0.6519 |
| short durations | highest fee | 0.9654 | 0.7925 |

Both rules lost revenue on average. Highest fee performed better for both
generators, especially with short durations, but its worst standard ratio was
0.4642. Shorter bookings made it more competitive, but not guaranteed optimal.

## 6. Time complexity

**Table 4. Complexity of the implemented functions.**

| Function | Complexity | Justification |
|---|---|---|
| `greedy_earliest_finish` | `O(n log n)` | One `O(n log n)` sort followed by a linear scan. |
| `greedy_highest_fee` | `O(n^2)` worst case | Sorting costs `O(n log n)`; each candidate may scan all accepted requests. |
| `best_schedule` | `O(n log n)` time, `O(n)` space | Sorting, `n` binary searches, linear DP, and linear reconstruction. |
| `brute_force` | about `O(2^n * n^2)` | Every subset is examined and its selected requests are sorted and checked. |

## 7. Testing summary

The suite covers empty, one-request, overlapping, non-overlapping, and
back-to-back cases; the supplied example; feasibility and fee totals for every
function; 600 seeded random inputs against brute force; 300 equal-fee inputs;
and greedy totals not exceeding the optimum. The two personal counterexample
tests are skipped because their constants remain `None`.

**Table 5. Pytest result and supplementary first-failure search.**

| Measurement | Result |
|---|---:|
| Pytest passed | 4 |
| Pytest skipped | 2 |
| Pytest failed | 0 |
| Earliest-finish random trials passed before first failure | 2 |
| Highest-fee random trials passed before first failure | 11 |

The run used Python 3.12.10 on Microsoft Windows 11 Pro 10.0.26200, 64-bit.
The separate search used the test generator and stopped at the first strict
greedy failure for each rule.

## 8. Critical reflection

### Testing is not proof of correctness

Earliest finish passed only 2 random trials before failure, while highest fee
passed 11. Passing tests is evidence about tested cases, not proof of
optimality. Brute force is stronger for small cases, but cannot turn a
heuristic into a general proof. The counterexamples expose the missing
optimality arguments.

### Should the manager keep a simple rule?

I would not use either greedy rule when maximum revenue matters. For the
standard generator, earliest finish averaged 0.8375 and highest fee 0.8643 of
optimal revenue; worst ratios were 0.5247 and 0.4642. With short durations,
highest fee improved to 0.9654 on average, but its worst ratio was 0.7925.
The `O(n log n)` dynamic program is the safer choice.

### Equal fees versus different fees

When every fee is equal, maximizing revenue means maximizing the number of
bookings. An earliest-finishing first booking leaves at least as much remaining
time as any other, so exchanging it into an optimum preserves later bookings.
With unequal fees, preserving the count is not enough: Table 1 has two
requests ending at 8 with fees 24 and 29, so the exchange argument fails.

