// Test driver for the Fenwick tree. Protocol:
//   n q
//   then q ops:  "u i d" -> update(i, d)   |   "q l r" -> print query_range(l, r)
#include <iostream>
#include "impl.cpp"
using namespace std;
int main() {
    int n, q;
    if (!(cin >> n >> q)) return 0;
    FenwickTree ft(n);
    for (int k = 0; k < q; k++) {
        char op; cin >> op;
        if (op == 'u') { int i, d; cin >> i >> d; ft.update(i, d); }
        else           { int l, r; cin >> l >> r; cout << ft.query_range(l, r) << "\n"; }
    }
    return 0;
}
