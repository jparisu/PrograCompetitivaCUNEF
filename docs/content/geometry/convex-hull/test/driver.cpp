// Protocol: n ; n points "x y"  ->  print number of hull vertices
#include <iostream>
#include <vector>
#include "impl.cpp"
using namespace std;
int main() {
    int n; if (!(cin >> n)) return 0;
    vector<P> pts(n);
    for (int i = 0; i < n; i++) cin >> pts[i].x >> pts[i].y;
    cout << convex_hull(pts).size() << "\n";
    return 0;
}
