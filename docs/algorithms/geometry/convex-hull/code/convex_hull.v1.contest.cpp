// AUTO-GENERATED from convex_hull.v1.clean.cpp — do not edit.
// To override, replace this file with a hand-written version (remove this marker).
#include <vector>
#include <algorithm>
using namespace std;
struct P {
    long long x, y;
    bool operator<(const P& o) const {
        return x < o.x || (x == o.x && y < o.y);
    }
};
long long cross(const P& O, const P& A, const P& B) {
    return (A.x - O.x) * (B.y - O.y) - (A.y - O.y) * (B.x - O.x);
}
vector<P> convex_hull(vector<P> pts) {
    int n = pts.size();
    if (n < 3) return pts;
    sort(pts.begin(), pts.end());
    vector<P> h(2 * n);
    int k = 0;
    for (int i = 0; i < n; i++) {
        while (k >= 2 && cross(h[k - 2], h[k - 1], pts[i]) <= 0) k--;
        h[k++] = pts[i];
    }
    for (int i = n - 2, t = k + 1; i >= 0; i--) {
        while (k >= t && cross(h[k - 2], h[k - 1], pts[i]) <= 0) k--;
        h[k++] = pts[i];
    }
    h.resize(k - 1);
    return h;
}
