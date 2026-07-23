// Protocol: n ; n sorted ints ; target  ->  print index of target, or -1
#include <iostream>
#include <vector>
#include "impl.cpp"
using namespace std;
int main() {
    int n; if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    int t; cin >> t;
    cout << binary_search_idx(a, t) << "\n";
    return 0;
}
