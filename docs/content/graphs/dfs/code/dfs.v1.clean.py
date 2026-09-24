#! AUTO-GENERATED from dfs.v1.full.py — do not edit.
#! To override, replace this file with a hand-written version (remove this marker).
def dfs_recursive(adj: list[list[int]], start: int) -> list[int]:
    visited: set[int] = set()
    traversal: list[int] = []

    def _dfs(node: int) -> None:
        visited.add(node)
        traversal.append(node)

        for neighbor in adj[node]:
            if neighbor not in visited:
                _dfs(neighbor)

    _dfs(start)
    return traversal

def dfs_iterative(adj: list[list[int]], start: int) -> list[int]:
    visited: set[int] = set()
    traversal: list[int] = []

    stack: list[int] = [start]

    while stack:
        node = stack.pop()

        if node not in visited:
            visited.add(node)
            traversal.append(node)

            for neighbor in reversed(adj[node]):
                if neighbor not in visited:
                    stack.append(neighbor)

    return traversal
