"""CSF302 Lab 7, Question 2: Huffman coding for byte strings."""

from __future__ import annotations

import heapq
import itertools
from collections import Counter
from pathlib import Path


class Node:
    def __init__(self, frequency: int, symbol: int | None = None, left: "Node | None" = None, right: "Node | None" = None):
        self.frequency = frequency
        self.symbol = symbol
        self.left = left
        self.right = right


def build_tree(data: bytes) -> Node | None:
    if not data:
        return None
    counter = itertools.count()
    heap: list[tuple[int, int, Node]] = []
    for symbol, frequency in Counter(data).items():
        heapq.heappush(heap, (frequency, next(counter), Node(frequency, symbol)))
    while len(heap) > 1:
        frequency1, _, left = heapq.heappop(heap)
        frequency2, _, right = heapq.heappop(heap)
        parent = Node(frequency1 + frequency2, left=left, right=right)
        heapq.heappush(heap, (parent.frequency, next(counter), parent))
    return heap[0][2]


def make_codes(root: Node | None) -> dict[int, str]:
    codes: dict[int, str] = {}
    if root is None:
        return codes
    def visit(node: Node, prefix: str) -> None:
        if node.symbol is not None:
            codes[node.symbol] = prefix or "0"
            return
        visit(node.left, prefix + "0")  # type: ignore[arg-type]
        visit(node.right, prefix + "1")  # type: ignore[arg-type]
    visit(root, "")
    return codes


def encode(data: bytes, codes: dict[int, str]) -> str:
    return "".join(codes[symbol] for symbol in data)


def decode(bits: str, root: Node | None) -> bytes:
    if root is None:
        return b""
    if root.symbol is not None:
        return bytes([root.symbol]) * len(bits)
    output = bytearray()
    node = root
    for bit in bits:
        node = node.left if bit == "0" else node.right  # type: ignore[assignment]
        if node.symbol is not None:  # type: ignore[union-attr]
            output.append(node.symbol)  # type: ignore[arg-type]
            node = root
    return bytes(output)


def is_prefix_free(codes: dict[int, str]) -> bool:
    values = list(codes.values())
    return all(not (a != b and b.startswith(a)) for a in values for b in values)


def analyse_file(path: Path) -> dict[str, object]:
    with path.open("rb") as file:
        data = file.read()
    root = build_tree(data)
    codes = make_codes(root)
    bits = encode(data, codes)
    decoded = decode(bits, root)
    assert decoded == data
    assert is_prefix_free(codes)
    frequencies = Counter(data)
    average = sum(frequencies[symbol] * len(code) for symbol, code in codes.items()) / len(data) if data else 0.0
    ratio = len(bits) / (8 * len(data)) if data else 0.0
    return {"path": str(path), "bytes": len(data), "codes": codes, "frequencies": frequencies, "bits": len(bits), "average": average, "ratio": ratio}


def print_analysis(result: dict[str, object]) -> None:
    print(f"\n{result['path']}: {result['bytes']} bytes, {result['bits']} encoded bits")
    print("symbol frequency code")
    frequencies: Counter[int] = result["frequencies"]  # type: ignore[assignment]
    codes: dict[int, str] = result["codes"]  # type: ignore[assignment]
    for symbol, code in sorted(codes.items(), key=lambda pair: (len(pair[1]), pair[1], pair[0])):
        print(repr(chr(symbol)), frequencies[symbol], code)
    print(f"average code length: {result['average']:.3f} bits/symbol")
    print(f"compression ratio (table cost excluded): {result['ratio']:.4f}")


def main() -> None:
    paths = [Path(argument) for argument in __import__("sys").argv[1:]]
    if not paths:
        paths = [Path("sample_english.txt"), Path("sample_source.py"), Path("sample_repeated.txt")]
    for path in paths:
        print_analysis(analyse_file(path))


if __name__ == "__main__":
    main()
