/**
 * Dijkstra — single-source shortest paths (non-negative weights).
 *
 * Greedily expands the closest unsettled node using a min-priority-queue.
 *
 * Input:  n (node count), adjacency list adj[u] = {(v, w), ...}, src.
 * Output: dist[i] = shortest distance from src to i, or INF if unreachable.
 * Complexity: O((V + E) log V).
 */
#include <vector>
#include <queue>
#include <functional>
using namespace std;

const long long INF = 1e18;

vector<long long> dijkstra(int n, const vector<vector<pair<int, int>>>& adj, int src) {
    vector<long long> dist(n, INF);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<>> pq;
    dist[src] = 0;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > dist[u]) continue;                 // stale entry
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
