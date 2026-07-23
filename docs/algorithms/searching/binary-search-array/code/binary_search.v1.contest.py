#! AUTO-GENERATED from binary_search.v1.clean.py — do not edit.
#! To override, replace this file with a hand-written version (remove this marker).
def binary_search(b, f):
    d = 0
    c = len(b) - 1
    while d <= c:
        e = (d + c) // 2
        if b[e] == f:
            return e
        if b[e] < f:
            d = e + 1
        else:
            c = e - 1
    return -1
