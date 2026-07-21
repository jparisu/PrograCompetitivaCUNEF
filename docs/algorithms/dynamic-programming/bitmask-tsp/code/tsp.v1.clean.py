# AUTO-GENERATED from tsp.v1.full.py — do not edit.
# To override, replace this file with a hand-written version (remove this marker).
INF = float("inf")
def tsp(dist):
    n = len(dist)
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1, 1 << n):
        for u in range(n):
            if dp[mask][u] == INF or not (mask & (1 << u)):
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                nmask = mask | (1 << v)
                cand = dp[mask][u] + dist[u][v]
                if cand < dp[nmask][v]:
                    dp[nmask][v] = cand
    full = (1 << n) - 1
    return min(dp[full][u] + dist[u][0] for u in range(n))
