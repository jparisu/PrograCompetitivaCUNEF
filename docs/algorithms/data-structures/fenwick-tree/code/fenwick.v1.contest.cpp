// AUTO-GENERATED from fenwick.v1.clean.cpp — do not edit.
// To override, replace this file with a hand-written version (remove this marker).
#include <vector>
using namespace std;
struct FenwickTree {
    int n;
    vector<int> tree;
    FenwickTree(int n) : n(n), tree(n) {}
    void update(int index, int delta) {
        for (index++; index <= n; index += index & -index)
            tree[index - 1] += delta;
    }
    int query(int index) {
        int acc = 0;
        for (; index > 0; index -= index & -index)
            acc += tree[index - 1];
        return acc;
    }
    int query_range(int l, int r) { return query(r) - query(l); }
};
