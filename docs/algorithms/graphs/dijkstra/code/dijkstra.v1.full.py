"""Dijkstra — single-source shortest paths (non-negative weights).

Greedily expands the closest unsettled node using a min-heap.

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
    dist: list[float] = [INF] * n
    dist[src] = 0
    pq: list[tuple[int, int]] = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:                            # stale entry
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist
