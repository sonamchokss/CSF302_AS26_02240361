"""Scheduling algorithms for the community-hall booking problem."""

from bisect import bisect_right
from itertools import combinations


def _with_indices(requests):
    """Return requests with their original input indices attached."""
    return [(start, finish, fee, index)
            for index, (start, finish, fee) in enumerate(requests)]


def greedy_earliest_finish(requests):
    """Accept compatible requests in increasing finish-time order."""
    indexed = _with_indices(requests)
    indexed.sort(key=lambda item: (item[1], item[0], item[2], item[3]))

    total = 0
    chosen = []
    last_finish = None
    for start, finish, fee, index in indexed:
        # Equality is allowed, so a request fits when start >= last_finish.
        if last_finish is None or start >= last_finish:
            chosen.append(index)
            total += fee
            last_finish = finish

    return total, sorted(chosen)


def greedy_highest_fee(requests):
    """Try requests from highest fee to lowest fee."""
    indexed = _with_indices(requests)
    indexed.sort(key=lambda item: (-item[2], item[1], item[0], item[3]))

    accepted = []
    total = 0
    for request in indexed:
        start, finish, fee, index = request
        # Check the candidate against every request already accepted.
        fits = all(finish <= other[0] or other[1] <= start
                   for other in accepted)
        if fits:
            accepted.append(request)
            total += fee

    return total, sorted(item[3] for item in accepted)


def best_schedule(requests):
    """Find a maximum-fee compatible schedule with dynamic programming."""
    indexed = _with_indices(requests)
    indexed.sort(key=lambda item: (item[1], item[0], item[2], item[3]))
    n = len(indexed)
    if n == 0:
        return 0, []

    finishes = [item[1] for item in indexed]
    compatible_before = []
    for j, request in enumerate(indexed):
        # Search only earlier requests: p(j) counts finishes <= start_j.
        compatible_before.append(bisect_right(finishes, request[0], hi=j))

    # dp[j] is the best fee using the first j requests in finish order.
    dp = [0] * (n + 1)
    for j in range(1, n + 1):
        start, finish, fee, index = indexed[j - 1]
        include = fee + dp[compatible_before[j - 1]]
        exclude = dp[j - 1]
        dp[j] = max(exclude, include)

    # Reconstruct by walking backwards through the same include/exclude cases.
    chosen = []
    j = n
    while j > 0:
        start, finish, fee, index = indexed[j - 1]
        if fee + dp[compatible_before[j - 1]] > dp[j - 1]:
            chosen.append(index)
            j = compatible_before[j - 1]
        else:
            j -= 1

    return dp[n], sorted(chosen)


def brute_force(requests):
    """Check every subset; intended for small inputs (n <= 15)."""
    n = len(requests)
    best_total = 0
    best_indices = []

    for mask in range(1 << n):
        indices = [i for i in range(n) if mask & (1 << i)]
        ordered = sorted(indices, key=lambda i: (requests[i][0],
                                                  requests[i][1], i))
        feasible = all(requests[ordered[pos]][1] <=
                       requests[ordered[pos + 1]][0]
                       for pos in range(len(ordered) - 1))
        if feasible:
            total = sum(requests[i][2] for i in indices)
            if total > best_total:
                best_total = total
                best_indices = indices

    return best_total, sorted(best_indices)

