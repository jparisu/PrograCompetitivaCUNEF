import sys
from impl import dijkstra
data = sys.stdin.read().split(); it = iter(data)
n = int(next(it)); m = int(next(it)); src = int(next(it))
adj = [[] for _ in range(n)]
for _ in range(m):
    u = int(next(it)); v = int(next(it)); w = int(next(it))
    adj[u].append((v, w))
d = dijkstra(n, adj, src)
print(" ".join(str(x if x != float("inf") else -1) for x in d))
