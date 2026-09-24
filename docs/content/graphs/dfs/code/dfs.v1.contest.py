#! AUTO-GENERATED from dfs.v1.clean.py — do not edit.
#! To override, replace this file with a hand-written version (remove this marker).
def dfs_recursive(b, f):
    h = set()
    g = []
    def a(d):
        h.add(d)
        g.append(d)
        for c in b[d]:
            if c not in h:
                a(c)
    a(f)
    return g
def dfs_iterative(b, f):
    h = set()
    g = []
    e = [f]
    while e:
        d = e.pop()
        if d not in h:
            h.add(d)
            g.append(d)
            for c in reversed(b[d]):
                if c not in h:
                    e.append(c)
    return g
