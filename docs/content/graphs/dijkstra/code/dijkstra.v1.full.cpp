/**
 * Dijkstra — single-source shortest paths (non-negative edge weights).
 *
 * Greedy idea: repeatedly settle the closest unsettled node. Because every
 * weight is non-negative, the instant a node is popped with the smallest
 * tentative distance that distance is already optimal — no not-yet-settled
 * node could offer a cheaper detour to it.
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
    // dist[u] = best distance to u found so far (INF until u is reached).
    vector<long long> dist(n, INF);

    // Min-priority-queue of (distance, node): greater<> keeps the smallest on top.
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<>> pq;

    dist[src] = 0;
    pq.push({0, src});

    while (!pq.empty()) {
        auto [d, u] = pq.top();   // u: closest unsettled node; d: its recorded distance
        pq.pop();

        // Lazy deletion: we never erase superseded heap entries, so an old,
        // larger distance for u may still be sitting in the queue. If d is worse
        // than the best known dist[u], this entry is stale — skip it.
        if (d > dist[u]) continue;

        // Relax every outgoing edge u -> v with weight w.
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {   // a shorter route to v goes through u
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});     // enqueue the improvement (old entry now stale)
            }
        }
    }
    return dist;
}
