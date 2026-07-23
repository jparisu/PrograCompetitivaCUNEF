#! AUTO-GENERATED from convex_hull.v1.full.py — do not edit.
#! To override, replace this file with a hand-written version (remove this marker).
def cross(o: tuple[int, int], a: tuple[int, int], b: tuple[int, int]) -> int:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
def convex_hull(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    pts: list[tuple[int, int]] = sorted(set(points))
    if len(pts) < 3:
        return pts
    lower: list[tuple[int, int]] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list[tuple[int, int]] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]
