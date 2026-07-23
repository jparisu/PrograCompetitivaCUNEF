/**
 * Fenwick Tree (Binary Indexed Tree).
 *
 * A structure for prefix sums with point updates: it stores an array and
 * answers range-sum queries and single-element updates, both in O(log n). Ideal
 * when the array keeps changing and range sums are needed many times.
 *
 * The public API is 0-based, but the tree is stored 1-based: cell `i` (1..n)
 * holds the sum of the half-open block (i - lowbit(i), i], where lowbit is the
 * lowest set bit of `i`. That block size is what lets both operations move in
 * O(log n) steps.
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
    vector<int> tree;  // 1-based cell i (stored at tree[i-1]) covers (i-lowbit(i), i]

    // Create a Fenwick tree of `n` elements, all zero.
    FenwickTree(int n) : n(n), tree(n) {}

    // Add `delta` to the element at `index` (0-based).
    void update(int index, int delta) {
        // `index++` converts to 1-based, then we walk UP: `index & -index`
        // isolates the lowest set bit, and adding it jumps to the next cell
        // whose block also contains this position (at most O(log n) cells).
        for (index++; index <= n; index += index & -index)
            tree[index - 1] += delta;
    }

    // Return the prefix sum of [0, index).
    int query(int index) {
        // A 0-based exclusive bound equals the 1-based element count, so no +1.
        // Walk DOWN: subtracting the lowest set bit jumps to the block just
        // before this one; the visited blocks tile [0, index) with no overlap.
        int acc = 0;
        for (; index > 0; index -= index & -index)
            acc += tree[index - 1];
        return acc;
    }

    // Return the sum of the half-open range [l, r).
    int query_range(int l, int r) { return query(r) - query(l); }
};
