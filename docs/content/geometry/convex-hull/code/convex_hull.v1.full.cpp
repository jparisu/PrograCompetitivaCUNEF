/**
 * Convex hull — Andrew's monotone chain.
 *
 * Computes the convex hull: the smallest convex polygon that contains a set of
 * 2D points (imagine a rubber band snapping around them).
 *
 * Input:  pts — a vector of 2D points (P{x, y}).
 * Output: the hull vertices in counter-clockwise order. Points lying *on* a hull
 *         edge (collinear) are dropped by the `<= 0` turn test, so only the
 *         corner vertices remain.
 * Complexity: O(n log n) time (dominated by the sort), O(n) space.
 */
#include <vector>
#include <algorithm>
using namespace std;

struct P {
    long long x, y;                          // 64-bit: cross() multiplies deltas
    bool operator<(const P& o) const {       // order the sweep by x, then by y
        return x < o.x || (x == o.x && y < o.y);
    }
};

// Cross product of vectors OA and OB. Its sign is the orientation of O->A->B:
//   > 0 left turn (counter-clockwise), < 0 right turn (clockwise), = 0 collinear.
long long cross(const P& O, const P& A, const P& B) {
    return (A.x - O.x) * (B.y - O.y) - (A.y - O.y) * (B.x - O.x);
}

vector<P> convex_hull(vector<P> pts) {
    int n = pts.size();
    if (n < 3) return pts;                    // 0-2 points: nothing to build
    sort(pts.begin(), pts.end());             // left-to-right sweep order

    vector<P> hull;                           // grows/shrinks like a stack
    // Lower hull: sweep left -> right, keeping only left turns.
    for (int i = 0; i < n; i++) {
        // Drop the last vertex while the edge does not turn left (right or
        // collinear): such a vertex lies inside the hull or on an edge.
        while (hull.size() >= 2 &&
               cross(hull[hull.size() - 2], hull.back(), pts[i]) <= 0)
            hull.pop_back();
        hull.push_back(pts[i]);
    }
    // Upper hull: sweep right -> left. `base` freezes the finished lower hull so
    // its vertices are never popped; pts[n-1] is skipped (already the last one).
    size_t base = hull.size() + 1;
    for (int i = n - 2; i >= 0; i--) {
        while (hull.size() >= base &&
               cross(hull[hull.size() - 2], hull.back(), pts[i]) <= 0)
            hull.pop_back();
        hull.push_back(pts[i]);
    }
    hull.pop_back();     // the last point repeats the starting vertex — drop it
    return hull;
}
