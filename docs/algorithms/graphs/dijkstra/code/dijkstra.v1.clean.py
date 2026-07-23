#! AUTO-GENERATED from dijkstra.v1.full.py — do not edit.
#! To override, replace this file with a hand-written version (remove this marker).
import heapq
def dijkstra(n: int, adj: list[list[tuple[int, int]]], src: int) -> list[int]:
    INF: float = float("inf")
    dist: list[float] = [INF] * n
    dist[src] = 0
    pq: list[tuple[int, int]] = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist
