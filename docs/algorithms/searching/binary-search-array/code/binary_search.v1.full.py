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
    hi: int = len(a) - 1
    while lo <= hi:
        mid: int = (lo + hi) // 2
        if a[mid] == target:
            return mid
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
