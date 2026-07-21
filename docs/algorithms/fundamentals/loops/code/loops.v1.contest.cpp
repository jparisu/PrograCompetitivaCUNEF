// AUTO-GENERATED from loops.v1.clean.cpp — do not edit.
// To override, replace this file with a hand-written version (remove this marker).
#include <iostream>
using namespace std;
int main() {
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
