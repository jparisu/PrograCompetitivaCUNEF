# Bucles [C++]

```{contents}
:local:
:depth: 2
```


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
    // Add value to the element at index (index starts on 0)
    void update(int index, int value) {
        index++;
        while (index <= n) {
            tree[index - 1] += value;
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
    // Return the sum from a to b (both included)
    int biquery(int a, int b) {
        return query_includes(b) - query(a);
    }

    vector<int> tree;
    int n;
};
```
