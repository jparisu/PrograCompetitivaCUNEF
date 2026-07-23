#! AUTO-GENERATED from convex_hull.v1.clean.py — do not edit.
#! To override, replace this file with a hand-written version (remove this marker).
def cross(f, c, d):
    return (c[0] - f[0]) * (d[1] - f[1]) - (c[1] - f[1]) * (d[0] - f[0])
def convex_hull(h):
    i = sorted(set(h))
    if len(i) < 3:
        return i
    e = []
    for g in i:
        while len(e) >= 2 and cross(e[-2], e[-1], g) <= 0:
            e.pop()
        e.append(g)
    j = []
    for g in reversed(i):
        while len(j) >= 2 and cross(j[-2], j[-1], g) <= 0:
            j.pop()
        j.append(g)
    return e[:-1] + j[:-1]
