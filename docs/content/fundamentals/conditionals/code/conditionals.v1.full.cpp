/**
 * Conditionals demo — print the larger of two numbers.
 *
 * Shows `if` / `else`: choosing what to do based on a condition.
 *
 * Input:  two integers a and b (separated by whitespace).
 * Output: the larger of the two (or either one when they are equal).
 */
#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;

    // Compare with `>`; the branch that runs is decided at run time.
    // (`a >= b` would also be correct here: on a tie we may print either one.)
    if (a > b) {
        cout << a << "\n";
    } else {
        cout << b << "\n";
    }
    return 0;
}
