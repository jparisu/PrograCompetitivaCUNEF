"""Binary search on a sorted list.

Finds a value in a **sorted** array by halving the search range at each step,
turning an O(n) scan into O(log n).

Args:
    a (list[int]): array sorted in non-decreasing order.
    target (int): value to look for.
Returns:
    int: an index ``i`` with ``a[i] == target``, or ``-1`` if it is not present.

Complexity: O(log n) time, O(1) space.
"""


def binary_search(a: list[int], target: int) -> int:
    lo: int = 0
    hi: int = len(a) - 1          # search the closed range [lo, hi]
    # Invariant: if target is in the array, it always lies within [lo, hi].
    while lo <= hi:               # stop only when the range is empty
        mid: int = (lo + hi) // 2  # Python ints never overflow, so this is safe
        if a[mid] == target:
            return mid            # found it
        if a[mid] < target:
            lo = mid + 1          # target is to the right; discard mid and left
        else:
            hi = mid - 1          # target is to the left; discard mid and right
    return -1                     # range emptied: target is not present
