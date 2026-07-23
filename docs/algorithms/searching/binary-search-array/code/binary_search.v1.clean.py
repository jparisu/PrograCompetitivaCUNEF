#! AUTO-GENERATED from binary_search.v1.full.py — do not edit.
#! To override, replace this file with a hand-written version (remove this marker).
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
