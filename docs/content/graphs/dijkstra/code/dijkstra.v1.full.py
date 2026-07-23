"""Dijkstra — single-source shortest paths (non-negative edge weights).

Greedy idea: repeatedly settle the closest unsettled node. Because every weight
is non-negative, once a node is popped with the smallest tentative distance that
distance is already optimal — no not-yet-settled node could offer a cheaper
detour to it.

Args:
    n (int): number of nodes (0..n-1).
    adj (list[list[tuple[int, int]]]): adj[u] = list of (v, weight) edges.
    src (int): source node.
Returns:
    list[int]: dist[i] = shortest distance src->i (float('inf') if unreachable).

Complexity: O((V + E) log V).
"""
import heapq


def dijkstra(n: int, adj: list[list[tuple[int, int]]], src: int) -> list[int]:
    INF: float = float("inf")
    dist: list[float] = [INF] * n            # dist[u] = best distance to u so far
    dist[src] = 0
    pq: list[tuple[int, int]] = [(0, src)]   # min-heap of (distance, node)
    while pq:
        d, u = heapq.heappop(pq)             # u: closest unsettled node
        # Lazy deletion: superseded entries are left in the heap. If d is worse
        # than the best known dist[u], this entry is stale — skip it.
        if d > dist[u]:
            continue
        for v, w in adj[u]:                  # relax each outgoing edge u -> v (weight w)
            if dist[u] + w < dist[v]:        # a shorter route to v goes through u
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))  # enqueue the improvement
    return dist
