/**
 * Loops demo — read n numbers and print their sum.
 *
 * Shows the two basic loops (`for` and `while`), the building block of almost
 * every program: repeat some work a number of times or until a condition holds.
 *
 * Input:  an integer n, then n integers.
 * Output: a single line with the sum of the n integers.
 */
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    long long sum = 0;
    for (int i = 0; i < n; i++) {   // `for`: known number of repetitions
        int x;
        cin >> x;
        sum += x;
    }

    cout << sum << "\n";
    return 0;
}
