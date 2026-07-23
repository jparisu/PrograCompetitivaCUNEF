"""Fenwick Tree (Binary Indexed Tree).

A structure for **prefix sums with point updates**: it stores an array and
answers range-sum queries and single-element updates, both in O(log n). Ideal
when the array keeps changing and range sums are needed many times.

The public API is 0-based, but the tree is stored 1-based: cell ``i`` (1..n)
holds the sum of the half-open block ``(i - lowbit(i), i]``, where ``lowbit`` is
the lowest set bit of ``i``. That block size is what lets both operations move
in O(log n) steps.

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
        index += 1  # switch to 1-based indexing
        while index <= self.n:
            self.tree[index - 1] += delta
            # `index & -index` isolates the lowest set bit; adding it walks UP
            # to the next cell whose block also contains this position.
            index += index & -index

    def query(self, index: int) -> int:
        """Prefix sum of the half-open range ``[0, index)``.

        Args:
            index (int): exclusive upper bound.
        Returns:
            int: sum of the elements in ``[0, index)``.
        """
        # A 0-based exclusive bound equals the 1-based element count, so no +1.
        acc: int = 0
        while index > 0:
            acc += self.tree[index - 1]
            # Subtract the lowest set bit to walk DOWN to the previous block;
            # the visited blocks tile [0, index) with no overlap.
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
