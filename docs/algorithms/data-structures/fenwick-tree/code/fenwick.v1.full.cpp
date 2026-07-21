/**
 * Fenwick Tree (Binary Indexed Tree).
 *
 * Prefix sums with point updates.
 *   build:  O(n)
 *   update: O(log n)   add `delta` at position `index`
 *   query:  O(log n)   prefix sum of [0, index)
 * Indices are 0-based.
 */
#include <vector>
using namespace std;

struct FenwickTree {
    int n;
    vector<int> tree;

    // Create a Fenwick tree of `n` elements, all zero.
    FenwickTree(int n) : n(n), tree(n) {}

    // Add `delta` to the element at `index`.
    void update(int index, int delta) {
        for (index++; index <= n; index += index & -index)
            tree[index - 1] += delta;
    }

    // Prefix sum of [0, index).
    int query(int index) {
        int acc = 0;
        for (; index > 0; index -= index & -index)
            acc += tree[index - 1];
        return acc;
    }

    // Sum of [l, r).
    int query_range(int l, int r) { return query(r) - query(l); }
};
