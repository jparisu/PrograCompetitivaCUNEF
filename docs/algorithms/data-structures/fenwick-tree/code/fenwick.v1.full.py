"""Fenwick Tree (Binary Indexed Tree).

A structure for **prefix sums with point updates**: it stores an array and
answers range-sum queries and single-element updates, both in O(log n). Ideal
when the array keeps changing and range sums are needed many times. Indices are
0-based.

    build:  O(n)   ·  update: O(log n)  ·  query: O(log n)  ·  space: O(n)
"""


class FenwickTree:
    def __init__(self, n: int) -> None:
        """Create a Fenwick tree of ``n`` elements, all zero.

        Args:
            n (int): number of elements.
        """
        self.n: int = n
        self.tree: list[int] = [0] * n

    def update(self, index: int, delta: int) -> None:
        """Add ``delta`` to the element at ``index``.

        Args:
            index (int): 0-based position to update.
            delta (int): amount to add.
        """
        index += 1
        while index <= self.n:
            self.tree[index - 1] += delta
            index += index & -index

    def query(self, index: int) -> int:
        """Prefix sum of the half-open range ``[0, index)``.

        Args:
            index (int): exclusive upper bound.
        Returns:
            int: sum of the elements in ``[0, index)``.
        """
        acc: int = 0
        while index > 0:
            acc += self.tree[index - 1]
            index -= index & -index
        return acc

    def query_range(self, l: int, r: int) -> int:
        """Sum of the half-open range ``[l, r)``.

        Args:
            l (int): inclusive lower bound.
            r (int): exclusive upper bound.
        Returns:
            int: sum of the elements in ``[l, r)``.
        """
        return self.query(r) - self.query(l)
