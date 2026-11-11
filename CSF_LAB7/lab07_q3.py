"""CSF302 Lab 7, Question 3: shortest paths and minimum spanning trees."""

from __future__ import annotations

import csv
import heapq
import random
import time
from pathlib import Path

Edge = tuple[int, int, float]


def read_graph(path: str | Path) -> tuple[int, list[Edge]]:
    """Read V E followed by u v w edges. Edges are directed for Dijkstra."""
    lines = Path(path).read_text().splitlines()
    vertices, edge_count = map(int, lines[0].split())
    edges = [tuple(map(float, line.split())) for line in lines[1:] if line.strip()]
    if len(edges) != edge_count:
        raise ValueError("edge count does not match the first line")
    return vertices, [(int(u), int(v), w) for u, v, w in edges]


def dijkstra(vertices: int, edges: list[Edge], source: int, finalise: bool = True) -> tuple[list[float], list[int | None]]:
    adjacency = [[] for _ in range(vertices)]
    for u, v, weight in edges:
        adjacency[u].append((v, weight))
    infinity = float("inf")
    distance = [infinity] * vertices
    parent: list[int | None] = [None] * vertices
    finalised = [False] * vertices
    distance[source] = 0
    heap = [(0.0, source)]
    while heap:
        current_distance, vertex = heapq.heappop(heap)
        if not finalise and current_distance != distance[vertex]:
            continue
        if finalise:
            if finalised[vertex]:
                continue
            finalised[vertex] = True
        for neighbour, weight in adjacency[vertex]:
            if finalise and finalised[neighbour]:
                continue
            new_distance = current_distance + weight
            if new_distance < distance[neighbour]:
                distance[neighbour] = new_distance
                parent[neighbour] = vertex
                heapq.heappush(heap, (new_distance, neighbour))
    return distance, parent


def build_path(parent: list[int | None], source: int, target: int) -> list[int]:
    path = []
    current: int | None = target
    while current is not None:
        path.append(current)
        if current == source:
            return path[::-1]
        current = parent[current]
    return []


class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, value: int) -> int:
        if self.parent[value] != value:
            self.parent[value] = self.find(self.parent[value])
        return self.parent[value]

    def union(self, first: int, second: int) -> bool:
        first_root, second_root = self.find(first), self.find(second)
        if first_root == second_root:
            return False
        if self.rank[first_root] < self.rank[second_root]:
            first_root, second_root = second_root, first_root
        self.parent[second_root] = first_root
        if self.rank[first_root] == self.rank[second_root]:
            self.rank[first_root] += 1
        return True


def kruskal(vertices: int, edges: list[Edge]) -> tuple[float, list[Edge]]:
    forest = UnionFind(vertices)
    chosen = []
    total = 0.0
    for edge in sorted(edges, key=lambda item: item[2]):
        if forest.union(edge[0], edge[1]):
            chosen.append(edge)
            total += edge[2]
            if len(chosen) == vertices - 1:
                break
    return total, chosen


def prim(vertices: int, edges: list[Edge]) -> tuple[float, list[Edge]]:
    adjacency = [[] for _ in range(vertices)]
    for u, v, weight in edges:
        adjacency[u].append((v, weight))
        adjacency[v].append((u, weight))
    chosen: list[Edge] = []
    visited = {0}
    heap = [(weight, 0, neighbour) for neighbour, weight in adjacency[0]]
    heapq.heapify(heap)
    total = 0.0
    while heap and len(chosen) < vertices - 1:
        weight, first, second = heapq.heappop(heap)
        if second in visited:
            continue
        visited.add(second)
        chosen.append((first, second, weight))
        total += weight
        for neighbour, next_weight in adjacency[second]:
            if neighbour not in visited:
                heapq.heappush(heap, (next_weight, second, neighbour))
    return total, chosen


def random_connected_graph(rng: random.Random, vertices: int, extra_edges: int) -> list[Edge]:
    edges: set[tuple[int, int]] = set()
    output: list[Edge] = []
    for vertex in range(1, vertices):
        parent = rng.randrange(vertex)
        edges.add((min(parent, vertex), max(parent, vertex)))
        output.append((parent, vertex, rng.randint(1, 100)))
    while len(output) < vertices - 1 + extra_edges:
        first, second = sorted((rng.randrange(vertices), rng.randrange(vertices)))
        if first != second and (first, second) not in edges:
            edges.add((first, second))
            output.append((first, second, rng.randint(1, 100)))
    return output


def benchmark(rng: random.Random, output_csv: Path, output_png: Path) -> None:
    for _ in range(100):
        vertices = rng.randint(5, 50)
        max_extra = vertices * (vertices - 1) // 2 - (vertices - 1)
        edges = random_connected_graph(rng, vertices, rng.randint(0, max_extra))
        total_k, chosen_k = kruskal(vertices, edges)
        total_p, chosen_p = prim(vertices, edges)
        assert len(chosen_k) == vertices - 1
        assert len(chosen_p) == vertices - 1
        assert total_k == total_p
    rows = []
    for label, extra in (("sparse", 2_000), ("dense", 250_000 - 1_000 + 1)):
        edges = random_connected_graph(rng, 1_000, extra)
        for algorithm in (kruskal, prim):
            times = []
            for _ in range(3):
                start = time.perf_counter()
                total, chosen = algorithm(1_000, edges)
                times.append(time.perf_counter() - start)
                assert len(chosen) == 999
            rows.append({"graph": label, "algorithm": algorithm.__name__, "edges": len(edges), "mean_seconds": sum(times) / len(times), "total": total})
    with output_csv.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    try:
        import matplotlib.pyplot as plt
        labels = ["sparse Kruskal", "sparse Prim", "dense Kruskal", "dense Prim"]
        values = [row["mean_seconds"] for row in rows]
        plt.figure(figsize=(7, 4))
        plt.bar(labels, values)
        plt.ylabel("seconds (algorithm only)")
        plt.title("Kruskal and Prim timing")
        plt.xticks(rotation=20)
        plt.tight_layout()
        plt.savefig(output_png, dpi=150)
        plt.close()
    except ImportError:
        print("matplotlib is not installed; timing CSV was still written.")


def bellman_ford(vertices: int, edges: list[Edge], source: int) -> list[float]:
    distance = [float("inf")] * vertices
    distance[source] = 0
    for _ in range(vertices - 1):
        changed = False
        for first, second, weight in edges:
            if distance[first] + weight < distance[second]:
                distance[second] = distance[first] + weight
                changed = True
        if not changed:
            break
    return distance


def main() -> None:
    graph_path = Path("sample_graph.txt")
    vertices, edges = read_graph(graph_path)
    distances, parents = dijkstra(vertices, edges, 0, finalise=True)
    print("Dijkstra from 0:")
    for vertex, distance in enumerate(distances):
        print(vertex, "unreachable" if distance == float("inf") else (distance, build_path(parents, 0, vertex)))
    total_k, chosen_k = kruskal(vertices, edges)
    total_p, chosen_p = prim(vertices, edges)
    print(f"MST Kruskal: {total_k} using {len(chosen_k)} edges")
    print(f"MST Prim: {total_p} using {len(chosen_p)} edges")
    negative_edges = [(0, 1, 2), (0, 2, 3), (2, 1, -2)]
    print("Negative-edge example:")
    for flag in (True, False):
        print(flag, dijkstra(3, negative_edges, 0, finalise=flag)[0])
    print("Bellman-Ford:", bellman_ford(3, negative_edges, 0))
    benchmark(random.Random(302), Path("q3_mst_timings.csv"), Path("q3_mst_timings.png"))


if __name__ == "__main__":
    main()
