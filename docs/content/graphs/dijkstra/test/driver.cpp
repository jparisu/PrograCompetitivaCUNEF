// Protocol: "n m src" ; m directed edges "u v w" -> print dist[0..n-1] (-1 if INF)
#include <iostream>
#include <vector>
#include "impl.cpp"
using namespace std;
int main() {
    int n, m, src;
    if (!(cin >> n >> m >> src)) return 0;
    vector<vector<pair<int, int>>> adj(n);
    for (int i = 0; i < m; i++) { int u, v, w; cin >> u >> v >> w; adj[u].push_back({v, w}); }
    vector<long long> d = dijkstra(n, adj, src);
    for (int i = 0; i < n; i++) cout << (d[i] >= INF ? -1 : d[i]) << (i + 1 < n ? ' ' : '\n');
    return 0;
}
