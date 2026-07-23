import sys
from impl import convex_hull
d = sys.stdin.read().split(); it = iter(d)
n = int(next(it))
pts = [(int(next(it)), int(next(it))) for _ in range(n)]
print(len(convex_hull(pts)))
