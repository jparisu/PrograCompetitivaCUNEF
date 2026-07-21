# AUTO-GENERATED from fenwick.v1.full.py — do not edit.
# To override, replace this file with a hand-written version (remove this marker).
class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * n
    def update(self, index, delta):
        index += 1
        while index <= self.n:
            self.tree[index - 1] += delta
            index += index & -index
    def query(self, index):
        acc = 0
        while index > 0:
            acc += self.tree[index - 1]
            index -= index & -index
        return acc
    def query_range(self, l, r):
        return self.query(r) - self.query(l)
