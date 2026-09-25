"""Depth-First Search (DFS) — Recursive and Iterative.

Computes the **DFS traversal**: explores as far as possible along each branch
before backtracking (imagine traversing a maze by always keeping your hand on
one wall until you hit a dead end, then retreating).

Complexity: O(V + E) time, O(V) space (where V is vertices and E is edges).
"""


def dfs_recursive(adj: list[list[int]], start: int) -> list[int]:
    """Depth-First Search traversal using recursion.

    Args:
        adj (list[list[int]]): Adjacency list representing the graph.
        start (int): The starting node index.
    Returns:
        list[int]: The nodes visited, in DFS traversal order.
    """
    visited: set[int] = set()
    traversal: list[int] = []

    def _dfs(node: int) -> None:
        visited.add(node)
        traversal.append(node)
        
        # Recur for all unvisited adjacent vertices
        for neighbor in adj[node]:
            if neighbor not in visited:
                _dfs(neighbor)

    _dfs(start)
    return traversal


def dfs_iterative(adj: list[list[int]], start: int) -> list[int]:
    """Depth-First Search traversal using an explicit stack.

    Args:
        adj (list[list[int]]): Adjacency list representing the graph.
        start (int): The starting node index.
    Returns:
        list[int]: The nodes visited, in DFS traversal order.
    """
    visited: set[int] = set()
    traversal: list[int] = []
    
    # Initialize the stack with the starting node
    stack: list[int] = [start]

    while stack:
        node = stack.pop()
        
        # A node might be added to the stack multiple times, so we check here
        if node not in visited:
            visited.add(node)
            traversal.append(node)
            
            # Push unvisited neighbors. Reversed to match the recursive 
            # left-to-right exploration order.
            for neighbor in reversed(adj[node]):
                if neighbor not in visited:
                    stack.append(neighbor)

    return traversal