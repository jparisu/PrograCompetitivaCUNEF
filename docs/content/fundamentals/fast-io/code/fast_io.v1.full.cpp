/**
 * Fast I/O — read many integers quickly and print their sum.
 *
 * `ios::sync_with_stdio(false)` + `cin.tie(nullptr)` unhook the C++ streams from
 * C stdio; on large inputs this is dramatically faster and avoids Time Limit
 * Exceeded.
 *
 * Input:  an integer n, then n integers.
 * Output: the sum of the n integers.
 */
#include <iostream>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    long long sum = 0;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        sum += x;
    }
    cout << sum << "\n";
    return 0;
}
