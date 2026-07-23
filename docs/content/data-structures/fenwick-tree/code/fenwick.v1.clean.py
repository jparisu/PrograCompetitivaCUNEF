#! AUTO-GENERATED from fenwick.v1.full.py — do not edit.
#! To override, replace this file with a hand-written version (remove this marker).
class FenwickTree:
    def __init__(self, n: int) -> None:
        self.n: int = n
        self.tree: list[int] = [0] * n

    def update(self, index: int, delta: int) -> None:
        index += 1
        while index <= self.n:
            self.tree[index - 1] += delta
            index += index & -index

    def query(self, index: int) -> int:
        acc: int = 0
        while index > 0:
            acc += self.tree[index - 1]
            index -= index & -index
        return acc

    def query_range(self, l: int, r: int) -> int:
        return self.query(r) - self.query(l)
