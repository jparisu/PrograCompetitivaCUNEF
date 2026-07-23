//! AUTO-GENERATED from convex_hull.v1.full.cpp — do not edit.
//! To override, replace this file with a hand-written version (remove this marker).
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

    vector<P> hull;
    for (int i = 0; i < n; i++) {
        while (hull.size() >= 2 &&
               cross(hull[hull.size() - 2], hull.back(), pts[i]) <= 0)
            hull.pop_back();
        hull.push_back(pts[i]);
    }
    size_t base = hull.size() + 1;
    for (int i = n - 2; i >= 0; i--) {
        while (hull.size() >= base &&
               cross(hull[hull.size() - 2], hull.back(), pts[i]) <= 0)
            hull.pop_back();
        hull.push_back(pts[i]);
    }
    hull.pop_back();
    return hull;
}
