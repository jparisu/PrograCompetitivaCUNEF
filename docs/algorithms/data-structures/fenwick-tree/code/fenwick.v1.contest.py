# AUTO-GENERATED from fenwick.v1.clean.py — do not edit.
# To override, replace this file with a hand-written version (remove this marker).
class FenwickTree:

    def __init__(self, e):
        self.n = e
        self.tree = [0] * e

    def update(self, c, b):
        c += 1
        while c <= self.n:
            self.tree[c - 1] += b
            c += c & -c

    def query(self, c):
        a = 0
        while c > 0:
            a += self.tree[c - 1]
            c -= c & -c
        return a

    def query_range(self, d, f):
        return self.query(f) - self.query(d)
