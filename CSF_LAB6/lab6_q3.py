"""CSF302 Lab 6, Question 3: LCS and line-based diff."""

import csv
import random
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt


def lcs_table(x, y):
    table = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]
    for i, left in enumerate(x, 1):
        for j, right in enumerate(y, 1):
            table[i][j] = table[i - 1][j - 1] + 1 if left == right else max(
                table[i - 1][j], table[i][j - 1]
            )
    return table


def reconstruct_lcs(x, y, table):
    result = []
    i, j = len(x), len(y)
    while i and j:
        if x[i - 1] == y[j - 1]:
            result.append(x[i - 1])
            i -= 1
            j -= 1
        elif table[i - 1][j] >= table[i][j - 1]:
            i -= 1  # Tie-break: prefer moving up.
        else:
            j -= 1
    return "".join(reversed(result))


def lcs_length_two_rows(x, y):
    previous = [0] * (len(y) + 1)
    for left in x:
        current = [0]
        for j, right in enumerate(y, 1):
            current.append(previous[j - 1] + 1 if left == right else max(previous[j], current[j - 1]))
        previous = current
    return previous[-1]


def is_subsequence(candidate, text):
    position = 0
    for character in text:
        if position < len(candidate) and candidate[position] == character:
            position += 1
    return position == len(candidate)


def brute_force_lcs(x, y):
    best = ""
    for mask in range(1 << len(x)):
        candidate = "".join(x[i] for i in range(len(x)) if mask & (1 << i))
        if len(candidate) > len(best) and is_subsequence(candidate, y):
            best = candidate
    return best


def line_diff(old_lines, new_lines):
    table = lcs_table(old_lines, new_lines)
    result = []
    i, j = len(old_lines), len(new_lines)
    reversed_lines = []
    while i or j:
        if i and j and old_lines[i - 1] == new_lines[j - 1]:
            reversed_lines.append(("  ", old_lines[i - 1]))
            i -= 1
            j -= 1
        elif i and (not j or table[i - 1][j] >= table[i][j - 1]):
            reversed_lines.append(("- ", old_lines[i - 1]))
            i -= 1
        else:
            reversed_lines.append(("+ ", new_lines[j - 1]))
            j -= 1
    return list(reversed(reversed_lines))


def benchmark():
    rng = random.Random(3026)
    rows = []
    for length in range(5, 19):
        dp_times, brute_times = [], []
        for _ in range(3):
            x = "".join(rng.choice("ABC") for _ in range(length))
            y = "".join(rng.choice("ABC") for _ in range(length))
            start = time.perf_counter()
            dp_value = lcs_length_two_rows(x, y)
            dp_times.append(time.perf_counter() - start)
            start = time.perf_counter()
            brute_value = len(brute_force_lcs(x, y))
            brute_times.append(time.perf_counter() - start)
            assert dp_value == brute_value == lcs_table(x, y)[-1][-1]
        rows.append([length, sum(dp_times) / len(dp_times), sum(brute_times) / len(brute_times)])
    return rows


def print_table(x, y, table):
    print("    " + " ".join(f"{character:>2}" for character in " " + y))
    for i, row in enumerate(table):
        label = " " if i == 0 else x[i - 1]
        print(f"{label:>2} " + " ".join(f"{value:>2}" for value in row))


def main():
    x, y = "ABCBDAB", "BDCABA"
    table = lcs_table(x, y)
    answer = reconstruct_lcs(x, y, table)
    assert table[-1][-1] == 4 and len(answer) == 4
    assert is_subsequence(answer, x) and is_subsequence(answer, y)
    assert lcs_length_two_rows(x, y) == len(brute_force_lcs(x, y)) == 4
    print("Q3 - LCS")
    print_table(x, y, table)
    print("LCS (tie-break: move up on equal values):", answer)

    rows = benchmark()
    output = Path(__file__).with_name("q3_results.csv")
    with output.open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["length", "dp_seconds", "brute_force_seconds"])
        writer.writerows(rows)
    plt.figure()
    lengths = [row[0] for row in rows]
    plt.plot(lengths, [row[1] for row in rows], marker="o", label="DP, two rows")
    plt.plot(lengths, [row[2] for row in rows], marker="o", label="Brute force")
    plt.yscale("log")
    plt.xlabel("String length")
    plt.ylabel("Average time (seconds, log scale)")
    plt.title("LCS: dynamic programming versus brute force")
    plt.legend()
    plt.tight_layout()
    plt.savefig(Path(__file__).with_name("q3_lcs_times.png"), dpi=150)
    print("\n| length | DP seconds | brute-force seconds |")
    print("|---:|---:|---:|")
    for length, dp, brute in rows:
        print(f"| {length} | {dp:.8f} | {brute:.8f} |")

    if len(sys.argv) == 3:
        old_path, new_path = map(Path, sys.argv[1:3])
    else:
        old_path = Path(__file__).with_name("demo_old.txt")
        new_path = Path(__file__).with_name("demo_new.txt")
        if not old_path.exists():
            old_path.write_text(
                "first line\nold line\nkeep line\ndeleted line\n",
                encoding="utf-8",
            )
        if not new_path.exists():
            new_path.write_text(
                "first line\nnew line\nkeep line\nadded line\n",
                encoding="utf-8",
            )
    old_lines = old_path.read_text(encoding="utf-8").splitlines()
    new_lines = new_path.read_text(encoding="utf-8").splitlines()
    print("\nLine diff:")
    for prefix, line in line_diff(old_lines, new_lines):
        print(prefix + line)


if __name__ == "__main__":
    main()
