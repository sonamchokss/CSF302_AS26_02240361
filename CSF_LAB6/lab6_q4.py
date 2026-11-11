"""CSF302 Lab 6, Question 4: optimal binary search tree."""


def optimal_bst(p, q):
    n = len(p)
    e = [[0.0] * (n + 2) for _ in range(n + 2)]
    w = [[0.0] * (n + 2) for _ in range(n + 2)]
    root = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 2):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]
    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            e[i][j] = float("inf")
            w[i][j] = w[i][j - 1] + p[j - 1] + q[j]
            for r in range(i, j + 1):
                candidate = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if candidate < e[i][j]:
                    e[i][j] = candidate
                    root[i][j] = r
    return e, w, root


def print_tree(root, i, j, indent=""):
    if i > j:
        print(f"{indent}d{i - 1}")
        return
    r = root[i][j]
    print(f"{indent}k{r}")
    print_tree(root, i, r - 1, indent + "  ")
    print_tree(root, r + 1, j, indent + "  ")


def main():
    p = [0.15, 0.10, 0.05, 0.10, 0.20]
    q = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10]
    e, w, root = optimal_bst(p, q)
    print("Q4 - Optimal BST")
    print(f"Expected search cost: {e[1][5]:.2f}")
    print("Optimal tree:")
    print_tree(root, 1, 5)
    print(f"w[1][5] (total probability): {w[1][5]:.2f}")


if __name__ == "__main__":
    main()
