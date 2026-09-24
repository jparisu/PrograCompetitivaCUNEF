/**
 * Depth-First Search (DFS) — Recursive and Iterative.
 *
 * Computes the DFS traversal: explores as far as possible along each branch
 * before backtracking (imagine traversing a maze by always keeping your hand on
 * one wall until you hit a dead end, then retreating).
 *
 * Complexity: O(V + E) time, O(V) space (where V is vertices and E is edges).
 */

#include <vector>
#include <stack>

using namespace std;

// Helper function for the recursive DFS
void _dfs(int node, const vector<vector<int>>& adj, vector<bool>& visited, vector<int>& traversal) {
    visited[node] = true;
    traversal.push_back(node);
    
    // Recur for all unvisited adjacent vertices
    for (int neighbor : adj[node]) {
        if (!visited[neighbor]) {
            _dfs(neighbor, adj, visited, traversal);
        }
    }
}

/**
 * Depth-First Search traversal using recursion.
 *
 * @param adj Adjacency list representing the graph.
 * @param start The starting node index.
 * @return The nodes visited, in DFS traversal order.
 */
vector<int> dfs_recursive(const vector<vector<int>>& adj, int start) {
    vector<bool> visited(adj.size(), false);
    vector<int> traversal;
    
    _dfs(start, adj, visited, traversal);
    return traversal;
}


/**
 * Depth-First Search traversal using an explicit stack.
 *
 * @param adj Adjacency list representing the graph.
 * @param start The starting node index.
 * @return The nodes visited, in DFS traversal order.
 */
vector<int> dfs_iterative(const vector<vector<int>>& adj, int start) {
    vector<bool> visited(adj.size(), false);
    vector<int> traversal;
    
    // Initialize the stack with the starting node
    stack<int> s;
    s.push(start);

    while (!s.empty()) {
        int node = s.top();
        s.pop();

        // A node might be added to the stack multiple times, so we check here
        if (!visited[node]) {
            visited[node] = true;
            traversal.push_back(node);

            // Push unvisited neighbors in reverse order to match 
            // the recursive left-to-right exploration order.
            for (auto it = adj[node].rbegin(); it != adj[node].rend(); ++it) {
                if (!visited[*it]) {
                    s.push(*it);
                }
            }
        }
    }

    return traversal;
}