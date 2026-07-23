/**
 * Loops demo — read n numbers and print their sum.
 *
 * Illustrates a `for` loop with the accumulator pattern: a variable declared
 * outside the loop (`sum`) is updated on every iteration. This is the building
 * block of almost every program: repeat some work a fixed number of times.
 *
 * Input:  an integer n, then n integers.
 * Output: a single line with the sum of the n integers.
 */
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;                       // how many numbers follow

    long long sum = 0;              // accumulator (long long avoids overflow)
    for (int i = 0; i < n; i++) {   // `for`: exactly n iterations, i = 0..n-1
        int x;
        cin >> x;                   // read the i-th number
        sum += x;                   // add it to the running total
    }

    cout << sum << "\n";
    return 0;
}
