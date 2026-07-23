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
    int lo = 0, hi = (int)a.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;   // avoids overflow vs (lo + hi) / 2
        if (a[mid] == target) return mid;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
