"""CSF302 Lab 7, Question 1: greedy activity selection and knapsack."""

from __future__ import annotations

import itertools
import random
from pathlib import Path

Activity = tuple[int, int]
Item = tuple[int, int]  # weight, value


def read_activities(path: str | None = None) -> list[Activity]:
    """Read one start/finish pair per line, from a file or standard input."""
    lines = Path(path).read_text().splitlines() if path else []
    if not path:
        print("Enter start finish pairs, one per line; press Enter on a blank line.")
        while True:
            line = input().strip()
            if not line:
                break
            lines.append(line)
    activities = []
    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(f"Bad activity line: {line!r}")
        start, finish = map(int, parts)
        if finish < start:
            raise ValueError("Finish must be at least start")
        activities.append((start, finish))
    return activities


def select_activities(activities: list[Activity], rule: str = "finish") -> list[Activity]:
    """Select a compatible set using finish, start, or duration order."""
    if rule == "finish":
        ordered = sorted(activities, key=lambda a: (a[1], a[0]))
    elif rule == "start":
        ordered = sorted(activities, key=lambda a: (a[0], a[1]))
    elif rule == "duration":
        ordered = sorted(activities, key=lambda a: (a[1] - a[0], a[0], a[1]))
    else:
        raise ValueError("rule must be finish, start, or duration")
    accepted: list[Activity] = []
    for activity in ordered:
        if all(activity[0] >= other[1] or activity[1] <= other[0] for other in accepted):
            accepted.append(activity)
    return accepted


def optimal_activity_count(activities: list[Activity]) -> int:
    """Brute-force optimum for small inputs."""
    best = 0
    for size in range(len(activities) + 1):
        for choice in itertools.combinations(activities, size):
            if all(
                choice[i][1] <= choice[j][0] or choice[j][1] <= choice[i][0]
                for i in range(len(choice))
                for j in range(i + 1, len(choice))
            ):
                best = max(best, size)
    return best


def fractional_knapsack(items: list[Item], capacity: int) -> tuple[list[float], float]:
    """Take items by decreasing value/weight ratio."""
    taken = [0.0] * len(items)
    remaining = capacity
    total = 0.0
    for index, (weight, value) in sorted(
        enumerate(items), key=lambda pair: pair[1][1] / pair[1][0], reverse=True
    ):
        amount = min(weight, remaining)
        taken[index] = amount / weight
        total += amount * value / weight
        remaining -= amount
        if remaining == 0:
            break
    return taken, total


def greedy_knapsack(items: list[Item], capacity: int) -> tuple[list[int], int]:
    """Apply the fractional ratio order, but take only whole items."""
    taken = [0] * len(items)
    remaining = capacity
    total = 0
    for index, (weight, value) in sorted(
        enumerate(items), key=lambda pair: pair[1][1] / pair[1][0], reverse=True
    ):
        if weight <= remaining:
            taken[index] = 1
            total += value
            remaining -= weight
    return taken, total


def dp_knapsack(items: list[Item], capacity: int) -> tuple[list[int], int]:
    """Solve 0/1 knapsack by dynamic programming and recover selected items."""
    table = [[0] * (capacity + 1) for _ in range(len(items) + 1)]
    for i, (weight, value) in enumerate(items, start=1):
        for cap in range(capacity + 1):
            table[i][cap] = table[i - 1][cap]
            if weight <= cap:
                table[i][cap] = max(table[i][cap], table[i - 1][cap - weight] + value)
    chosen = [0] * len(items)
    cap = capacity
    for i in range(len(items), 0, -1):
        if table[i][cap] != table[i - 1][cap]:
            chosen[i - 1] = 1
            cap -= items[i - 1][0]
    return chosen, table[-1][-1]


def find_activity_counterexamples(rng: random.Random) -> dict[str, tuple[list[Activity], list[Activity], list[Activity]]]:
    """Find examples where start and duration ordering lose to finish ordering."""
    found: dict[str, tuple[list[Activity], list[Activity], list[Activity]]] = {}
    while len(found) < 2:
        count = rng.randint(3, 6)
        activities = []
        for _ in range(count):
            start = rng.randint(0, 10)
            activities.append((start, start + rng.randint(1, 6)))
        finish = select_activities(activities, "finish")
        for rule in ("start", "duration"):
            alternative = select_activities(activities, rule)
            if len(alternative) < len(finish):
                found.setdefault(rule, (activities, finish, alternative))
    return found


def run_experiments(seed: int = 302) -> dict[str, object]:
    rng = random.Random(seed)
    counterexamples = find_activity_counterexamples(rng)
    for _ in range(500):
        activities = [
            (start := rng.randint(0, 10), start + rng.randint(1, 6))
            for _ in range(rng.randint(3, 6))
        ]
        assert len(select_activities(activities, "finish")) == optimal_activity_count(activities)

    worst_ratio = 1.0
    worst_instance: tuple[list[Item], int, int, int] | None = None
    for _ in range(5000):
        items = [(rng.randint(1, 20), rng.randint(1, 50)) for _ in range(rng.randint(3, 10))]
        capacity = rng.randint(1, sum(weight for weight, _ in items))
        _, greedy_value = greedy_knapsack(items, capacity)
        _, optimal_value = dp_knapsack(items, capacity)
        _, fractional_value = fractional_knapsack(items, capacity)
        assert greedy_value <= optimal_value + 1e-9 <= fractional_value + 1e-9
        ratio = greedy_value / optimal_value if optimal_value else 1.0
        if ratio < worst_ratio:
            worst_ratio = ratio
            worst_instance = (items, capacity, greedy_value, optimal_value)
    return {
        "counterexamples": counterexamples,
        "worst_ratio": worst_ratio,
        "worst_instance": worst_instance,
    }


def main() -> None:
    print("Activity selection: enter a file path or press Enter for keyboard input.")
    path = input("Path (blank for keyboard): ").strip()
    if path:
        activities = read_activities(path)
        print("Earliest finish:", select_activities(activities, "finish"))
    results = run_experiments()
    for rule, (activities, finish, alternative) in results["counterexamples"].items():
        print(f"\nCounterexample for {rule}: {activities}")
        print("  earliest finish:", finish)
        print(f"  {rule}:", alternative)
    print("\nWorst random greedy 0/1 ratio found:", results["worst_ratio"])
    print("Worst instance (items, capacity, greedy, optimum):", results["worst_instance"])
    items = [(10, 60), (20, 100), (30, 120)]
    print("\nFractional example:", fractional_knapsack(items, 50))
    print("Hand-built poor 0/1 example (capacity 50):", greedy_knapsack([(10, 60), (20, 100), (30, 120)], 50), dp_knapsack(items, 50))


if __name__ == "__main__":
    main()
