# Fenwick Tree (BIT)

!!! info "Metadata"
    **Level:** Intermediate · **Difficulty:** 3.0 · **Complexity:** O(log n) per operation

A **Fenwick tree** (or *Binary Indexed Tree*) maintains prefix sums of an array while
allowing **point updates** and **range queries**, both in **O(log n)**. It is the ideal
structure when the array changes and we need range sums many times.

## Code

=== "C++"
    ```cpp
    --8<-- "algorithms/data-structures/fenwick-tree/code/fenwick.v1.full.cpp"
    ```
=== "Python"
    ```python
    --8<-- "algorithms/data-structures/fenwick-tree/code/fenwick.v1.full.py"
    ```

!!! note "`clean` and `contest` versions"
    In the next phase, the comment-free (`clean`) and compressed (`contest`) versions
    will be generated automatically.

## Complexity

| Operation | Complexity |
|-----------|------------|
| Build | O(n) |
| `update` | O(log n) |
| `query` | O(log n) |
| Memory | O(n) |

## Practice

| Name | Difficulty | Link |
|------|------------|------|
| fenwick | 4.0 | [Kattis](https://open.kattis.com/problems/fenwick) |
| supercomputer | 2.7 | [Kattis](https://open.kattis.com/problems/supercomputer) |

## References

- [CP-Algorithms: Fenwick Tree](https://cp-algorithms.com/data_structures/fenwick.html)
