/**
 * Fenwick Tree (Binary Indexed Tree).
 *
 * A structure for prefix sums with point updates: it stores an array and
 * answers range-sum queries and single-element updates, both in O(log n). Ideal
 * when the array keeps changing and range sums are needed many times. Indices
 * are 0-based.
 *
 *   FenwickTree(n)        build an empty tree of n zeros            O(n)
 *   update(index, delta)  add `delta` at position `index`          O(log n)
 *   query(index)          -> prefix sum of [0, index)              O(log n)
 *   query_range(l, r)     -> sum of [l, r)                         O(log n)
 */
#include <vector>
using namespace std;

struct FenwickTree {
    int n;
    vector<int> tree;

    // Create a Fenwick tree of `n` elements, all zero.
    FenwickTree(int n) : n(n), tree(n) {}

    // Add `delta` to the element at `index` (0-based).
    void update(int index, int delta) {
        for (index++; index <= n; index += index & -index)
            tree[index - 1] += delta;
    }

    // Return the prefix sum of [0, index).
    int query(int index) {
        int acc = 0;
        for (; index > 0; index -= index & -index)
            acc += tree[index - 1];
        return acc;
    }

    // Return the sum of [l, r).
    int query_range(int l, int r) { return query(r) - query(l); }
};
