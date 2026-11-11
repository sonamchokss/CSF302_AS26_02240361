"""CSF302 Lab 6, Question 2: matrix-chain multiplication."""

import csv
import random
from pathlib import Path


def matrix_chain_order(dimensions):
    count = len(dimensions) - 1
    cost = [[0] * (count + 1) for _ in range(count + 1)]
    split = [[0] * (count + 1) for _ in range(count + 1)]
    for length in range(2, count + 1):
        for i in range(1, count - length + 2):
            j = i + length - 1
            cost[i][j] = float("inf")
            for k in range(i, j):
                candidate = (
                    cost[i][k]
                    + cost[k + 1][j]
                    + dimensions[i - 1] * dimensions[k] * dimensions[j]
                )
                if candidate < cost[i][j]:
                    cost[i][j] = candidate
                    split[i][j] = k
    return cost[1][count], split


def parenthesize(split, i, j):
    if i == j:
        return f"A{i}"
    k = split[i][j]
    return f"({parenthesize(split, i, k)}{parenthesize(split, k + 1, j)})"


def brute_force(dimensions, i=1, j=None):
    if j is None:
        j = len(dimensions) - 1
    if i == j:
        return 0
    return min(
        brute_force(dimensions, i, k)
        + brute_force(dimensions, k + 1, j)
        + dimensions[i - 1] * dimensions[k] * dimensions[j]
        for k in range(i, j)
    )


def left_to_right(dimensions):
    total = 0
    for i in range(1, len(dimensions) - 1):
        total += dimensions[0] * dimensions[i] * dimensions[i + 1]
    return total


def main():
    rng = random.Random(3026)
    tests = [
        [30, 35, 15, 5, 10, 20, 25],
        [5, 4, 6, 2, 7],
    ]
    for _ in range(5):
        tests.append([rng.randint(1, 50) for _ in range(rng.randint(3, 9))])

    rows = []
    print("Q2 - Matrix-chain multiplication")
    for index, dimensions in enumerate(tests, 1):
        optimal, split = matrix_chain_order(dimensions)
        brute = brute_force(dimensions)
        assert optimal == brute
        left = left_to_right(dimensions)
        ratio = left / optimal if optimal else float("inf")
        expression = parenthesize(split, 1, len(dimensions) - 1)
        print(
            f"test {index}: dimensions={dimensions}, optimal={optimal}, "
            f"left_to_right={left}, ratio={ratio:.4f}, order={expression}"
        )
        rows.append([index, dimensions, optimal, left, ratio, expression])

    output = Path(__file__).with_name("q2_results.csv")
    with output.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["test", "dimensions", "optimal_cost", "left_to_right_cost", "ratio", "parenthesization"])
        writer.writerows(rows)
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
