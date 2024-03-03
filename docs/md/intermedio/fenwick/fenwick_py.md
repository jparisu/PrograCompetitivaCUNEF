# Fenwick [Python]

```py
class FenwickTree:

    # O(N)
    # Create a Fenwick tree with n elements, all initialized to zero
    def __init__(self, size):
        self.size = size
        self.tree = [0] * (size)

    # O(logN)
    # Add delta to the element at index (index starts on 0)
    def update(self, index, delta):
        index += 1
        while index <= self.size:
            self.tree[index - 1] += delta
            index += index & -index

    # O(logN)
    # Return the sum from 0 to index (no included) (index starts on 0)
    def query(self, index):
        acc = 0
        while index > 0:
            acc += self.tree[index - 1]
            index -= index & -index
        return acc

    # O(logN)
    # Return the sum from 0 to index (included) (index starts on 0)
    def query_includes(self, index):
        acc = 0
        index += 1
        while index > 0:
            acc += self.tree[index - 1]
            index -= index & -index
        return acc

    # O(logN)
    # Return the sum from start to end (both included) (index starts on 0)
    def query_range(self, start, end):
        return self.query_includes(end) - self.query(start)
```
