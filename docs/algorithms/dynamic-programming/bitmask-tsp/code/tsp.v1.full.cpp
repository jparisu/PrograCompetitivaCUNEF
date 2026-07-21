/**
 * Bitmask DP — Travelling Salesman Problem (Held-Karp).
 *
 * Minimum cost of a Hamiltonian cycle that starts and ends at node 0,
 * visiting every node exactly once. `dist` is an n x n cost matrix.
 *   time:  O(2^n * n^2)
 *   space: O(2^n * n)
 *
 * State: dp[mask][u] = min cost of a path that started at 0, visited exactly
 * the nodes in `mask`, and currently sits at `u`.
 */
#include <vector>
#include <algorithm>
using namespace std;

const long long INF = 1e18;

long long tsp(const vector<vector<long long>>& dist) {
    int n = dist.size();
    vector<vector<long long>> dp(1 << n, vector<long long>(n, INF));
    dp[1][0] = 0;                                  // start at node 0

    for (int mask = 1; mask < (1 << n); mask++) {
        for (int u = 0; u < n; u++) {
            if (dp[mask][u] == INF || !(mask & (1 << u))) continue;
            for (int v = 0; v < n; v++) {
                if (mask & (1 << v)) continue;     // v already visited
                int nmask = mask | (1 << v);
                dp[nmask][v] = min(dp[nmask][v], dp[mask][u] + dist[u][v]);
            }
        }
    }

    long long ans = INF;
    int full = (1 << n) - 1;
    for (int u = 0; u < n; u++)
        ans = min(ans, dp[full][u] + dist[u][0]);  // close the cycle back to 0
    return ans;
}
