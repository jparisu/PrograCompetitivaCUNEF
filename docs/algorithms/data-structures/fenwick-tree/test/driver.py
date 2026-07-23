import sys
from impl import FenwickTree

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it)); q = int(next(it))
    ft = FenwickTree(n)
    out = []
    for _ in range(q):
        op = next(it)
        if op == "u":
            i = int(next(it)); d = int(next(it)); ft.update(i, d)
        else:
            l = int(next(it)); r = int(next(it)); out.append(str(ft.query_range(l, r)))
    sys.stdout.write("\n".join(out))
    if out:
        sys.stdout.write("\n")

main()
