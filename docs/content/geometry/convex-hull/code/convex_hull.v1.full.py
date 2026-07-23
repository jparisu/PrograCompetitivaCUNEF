"""Convex hull — Andrew's monotone chain.

Computes the **convex hull**: the smallest convex polygon that contains a set of
2D points (imagine a rubber band snapping around them). Points are ``(x, y)``
tuples. Points lying *on* a hull edge (collinear) are dropped, so only the corner
vertices remain; the result is returned in counter-clockwise order.

Complexity: O(n log n) time (dominated by the sort), O(n) space.
"""


def cross(o: tuple[int, int], a: tuple[int, int], b: tuple[int, int]) -> int:
    """Cross product of vectors OA and OB.

    Args:
        o, a, b (tuple[int, int]): 2D points.
    Returns:
        int: > 0 if O->A->B turns left (CCW), < 0 if it turns right, 0 if collinear.
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Convex hull of a set of points (Andrew's monotone chain).

    Args:
        points (list[tuple[int, int]]): the input points.
    Returns:
        list[tuple[int, int]]: the hull vertices, in counter-clockwise order.
    """
    # Sort by (x, y) and drop duplicates; the sweep needs a left-to-right order.
    pts: list[tuple[int, int]] = sorted(set(points))
    if len(pts) < 3:
        return pts                       # 0-2 distinct points: nothing to build

    # Lower hull: sweep left -> right, keeping only left turns. We pop the last
    # vertex while the edge does not turn left (right turn or collinear point).
    lower: list[tuple[int, int]] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Upper hull: the same sweep in reverse builds the other half.
    upper: list[tuple[int, int]] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenate; drop each chain's last point (it repeats the other's start).
    return lower[:-1] + upper[:-1]
