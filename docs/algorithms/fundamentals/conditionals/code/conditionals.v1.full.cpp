/**
 * Conditionals demo — print the larger of two numbers.
 *
 * Shows `if` / `else`: choosing what to do based on a condition.
 *
 * Input:  two integers a and b.
 * Output: the larger of the two.
 */
#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    if (a > b) cout << a << "\n";
    else       cout << b << "\n";
    return 0;
}
