# Fenwick [C++]

```cpp
#include <iostream>
#include <vector>
using namespace std;

struct FenwickTree {

    // O(N)
    // Create a Fenwick tree with n elements, all initialized to zero
    FenwickTree(int size)
        : n(size)
        , tree(size)
    {}

    // O(logN)
    // Add delta to the element at index (index starts on 0)
    void update(int index, int delta) {
        index++;
        while (index <= n) {
            tree[index - 1] += delta;
            index += index & -index;
        }
    }

    // O(logN)
    // Return the sum from 0 to index (no included) (index starts on 0)
    int query(int index) {
        int acc = 0;
        while (index > 0) {
            acc += tree[index - 1];
            index -= index & -index;
        }
        return acc;
    }

    // O(logN)
    // Return the sum from 0 to index (included) (index starts on 0)
    int query_includes(int index) {
        int acc = 0;
        index++;
        while (index > 0) {
            acc += tree[index - 1];
            index -= index & -index;
        }
        return acc;
    }

    // O(logN)
    // Return the sum from start to end (both included) (index starts on 0)
    int query_range(int start, int end) {
        return query_includes(end) - query(start);
    }

    vector<int> tree;
    int n;
};
```
