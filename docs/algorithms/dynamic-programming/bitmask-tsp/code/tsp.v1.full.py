"""Bitmask DP — Travelling Salesman Problem (Held-Karp).

Minimum cost of a Hamiltonian cycle that starts and ends at node 0, visiting
every node exactly once. `dist` is an n x n cost matrix.
    time:  O(2^n * n^2)
    space: O(2^n * n)

State: dp[mask][u] = min cost of a path that started at 0, visited exactly the
nodes in `mask`, and currently sits at `u`.
"""
INF = float("inf")


def tsp(dist):
    n = len(dist)
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0                                   # start at node 0

    for mask in range(1, 1 << n):
        for u in range(n):
            if dp[mask][u] == INF or not (mask & (1 << u)):
                continue
            for v in range(n):
                if mask & (1 << v):                # v already visited
                    continue
                nmask = mask | (1 << v)
                cand = dp[mask][u] + dist[u][v]
                if cand < dp[nmask][v]:
                    dp[nmask][v] = cand

    full = (1 << n) - 1
    return min(dp[full][u] + dist[u][0] for u in range(n))  # close the cycle
