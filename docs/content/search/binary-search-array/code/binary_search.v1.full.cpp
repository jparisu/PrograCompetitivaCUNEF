/**
 * Binary search on a sorted vector.
 *
 * Finds a value in a sorted array by halving the search range at each step,
 * turning an O(n) scan into O(log n).
 *
 * Input:  a — vector sorted in non-decreasing order; target — value to find.
 * Output: an index i with a[i] == target, or -1 if target is not present.
 * Complexity: O(log n) time, O(1) space.
 */
#include <vector>
using namespace std;

int binary_search_idx(const vector<int>& a, int target) {
    int lo = 0, hi = (int)a.size() - 1;    // search the closed range [lo, hi]
    // Invariant: if target is in the array, it always lies within [lo, hi].
    while (lo <= hi) {                      // stop only when the range is empty
        int mid = lo + (hi - lo) / 2;       // same as (lo+hi)/2, but never overflows int
        if (a[mid] == target) return mid;   // found it
        if (a[mid] < target) lo = mid + 1;  // target is to the right; discard mid and left
        else                 hi = mid - 1;  // target is to the left; discard mid and right
    }
    return -1;                              // range emptied: target is not present
}
