"""Fenwick Tree (Binary Indexed Tree).

Prefix sums with point updates.
    build:  O(n)
    update: O(log n)   add `delta` at position `index`
    query:  O(log n)   prefix sum of [0, index)
Indices are 0-based.
"""


class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * n

    def update(self, index, delta):
        """Add `delta` to the element at `index`."""
        index += 1
        while index <= self.n:
            self.tree[index - 1] += delta
            index += index & -index

    def query(self, index):
        """Prefix sum of [0, index)."""
        acc = 0
        while index > 0:
            acc += self.tree[index - 1]
            index -= index & -index
        return acc

    def query_range(self, l, r):
        """Sum of [l, r)."""
        return self.query(r) - self.query(l)
