# AUTO-GENERATED from tsp.v1.clean.py — do not edit.
# To override, replace this file with a hand-written version (remove this marker).
INF = float('inf')

def tsp(b):
    f = len(b)
    c = [[INF] * f for _ in range(1 << f)]
    c[1][0] = 0
    for e in range(1, 1 << f):
        for h in range(f):
            if c[e][h] == INF or not e & 1 << h:
                continue
            for i in range(f):
                if e & 1 << i:
                    continue
                g = e | 1 << i
                a = c[e][h] + b[h][i]
                if a < c[g][i]:
                    c[g][i] = a
    d = (1 << f) - 1
    return min((c[d][h] + b[h][0] for h in range(f)))
