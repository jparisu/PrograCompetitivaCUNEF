#! AUTO-GENERATED from dijkstra.v1.clean.py — do not edit.
#! To override, replace this file with a hand-written version (remove this marker).
import heapq
def dijkstra(f, b, h):
    a = float('inf')
    e = [a] * f
    e[h] = 0
    g = [(0, h)]
    while g:
        c, i = heapq.heappop(g)
        if c > e[i]:
            continue
        for j, k in b[i]:
            if e[i] + k < e[j]:
                e[j] = e[i] + k
                heapq.heappush(g, (e[j], j))
    return e
