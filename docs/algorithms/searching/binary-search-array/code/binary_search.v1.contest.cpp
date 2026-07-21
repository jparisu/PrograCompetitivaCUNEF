// AUTO-GENERATED from binary_search.v1.clean.cpp — do not edit.
// To override, replace this file with a hand-written version (remove this marker).
#include <vector>
using namespace std;
int binary_search_idx(const vector<int>& a, int target) {
    int lo = 0, hi = (int)a.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
