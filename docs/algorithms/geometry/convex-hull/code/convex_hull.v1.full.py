"""Convex hull — Andrew's monotone chain.

Returns the vertices of the convex hull in counter-clockwise order.
    time:  O(n log n)   (dominated by the sort)
    space: O(n)
Points are (x, y) tuples. Collinear points on the hull edges are removed.
"""


def cross(o, a, b):
    """Cross product OA x OB. >0 left turn, <0 right turn, =0 collinear."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points):
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenate, dropping the last point of each (it repeats the other's start).
    return lower[:-1] + upper[:-1]
