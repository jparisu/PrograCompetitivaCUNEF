//! AUTO-GENERATED from dfs.v1.clean.cpp — do not edit.
//! To override, replace this file with a hand-written version (remove this marker).
#include <vector>
#include <stack>
using namespace std;
void _dfs(int node, const vector<vector<int>>& adj, vector<bool>& visited, vector<int>& traversal) {
    visited[node] = true;
    traversal.push_back(node);
    for (int neighbor : adj[node]) {
        if (!visited[neighbor]) {
            _dfs(neighbor, adj, visited, traversal);
        }
    }
}
vector<int> dfs_recursive(const vector<vector<int>>& adj, int start) {
    vector<bool> visited(adj.size(), false);
    vector<int> traversal;
    _dfs(start, adj, visited, traversal);
    return traversal;
}
vector<int> dfs_iterative(const vector<vector<int>>& adj, int start) {
    vector<bool> visited(adj.size(), false);
    vector<int> traversal;
    stack<int> s;
    s.push(start);
    while (!s.empty()) {
        int node = s.top();
        s.pop();
        if (!visited[node]) {
            visited[node] = true;
            traversal.push_back(node);
            for (auto it = adj[node].rbegin(); it != adj[node].rend(); ++it) {
                if (!visited[*it]) {
                    s.push(*it);
                }
            }
        }
    }
    return traversal;
}
