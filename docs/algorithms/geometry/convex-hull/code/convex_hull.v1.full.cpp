/**
 * Convex hull — Andrew's monotone chain.
 *
 * Computes the convex hull: the smallest convex polygon that contains a set of
 * 2D points (imagine a rubber band snapping around them).
 *
 * Input:  pts — a vector of 2D points (P{x, y}).
 * Output: the hull vertices in counter-clockwise order; collinear points on the
 *         hull edges are removed (strict `<= 0` test).
 * Complexity: O(n log n) time (dominated by the sort), O(n) space.
 */
#include <vector>
#include <algorithm>
using namespace std;

struct P {
    long long x, y;
    bool operator<(const P& o) const {
        return x < o.x || (x == o.x && y < o.y);
    }
};

// Cross product of vectors OA and OB: >0 left turn, <0 right turn, =0 collinear.
long long cross(const P& O, const P& A, const P& B) {
    return (A.x - O.x) * (B.y - O.y) - (A.y - O.y) * (B.x - O.x);
}

vector<P> convex_hull(vector<P> pts) {
    int n = pts.size();
    if (n < 3) return pts;
    sort(pts.begin(), pts.end());

    vector<P> h(2 * n);
    int k = 0;
    // Lower hull.
    for (int i = 0; i < n; i++) {
        while (k >= 2 && cross(h[k - 2], h[k - 1], pts[i]) <= 0) k--;
        h[k++] = pts[i];
    }
    // Upper hull.
    for (int i = n - 2, t = k + 1; i >= 0; i--) {
        while (k >= t && cross(h[k - 2], h[k - 1], pts[i]) <= 0) k--;
        h[k++] = pts[i];
    }
    h.resize(k - 1);   // last point equals the first
    return h;
}
