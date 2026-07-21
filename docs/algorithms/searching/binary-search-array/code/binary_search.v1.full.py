"""Binary search on a sorted list.

Returns an index i with a[i] == target, or -1 if target is not present.
    time:  O(log n)
    space: O(1)
Precondition: `a` is sorted in non-decreasing order.
"""


def binary_search(a, target):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
