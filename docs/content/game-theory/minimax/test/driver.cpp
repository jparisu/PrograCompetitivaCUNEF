// Coins game driver for the generic minimax.
//
// Coins game: a row of coins is given; players alternate taking 1 or 2 coins
// from the LEFT and keep their value. Both play optimally; the starting player
// maximizes the coins they collect (zero-sum: the opponent minimizes them).
//
// Protocol:
//   line 1: the coin values, space-separated   (e.g. "2 3 5 8")
//   line 2: the starting (maximizing) player    (e.g. "1")
// Prints: "<best_value> <best_move>"  where best_move is 0 (take 1) or 1 (take 2).
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <tuple>
#include <functional>
#include "impl.cpp"
using namespace std;

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    vector<long long> coins;
    { istringstream ss(line); long long x; while (ss >> x) coins.push_back(x); }
    int start = 1;
    if (getline(cin, line)) { istringstream ss(line); ss >> start; }
    int n = (int) coins.size();

    // State = (i, max_to_move, max_score): coins already taken from the left,
    // whether the maximizing (starting) player moves now, and how many coins
    // that player has collected so far.
    typedef tuple<int, bool, long long> State;

    function<vector<State>(const State&)> possible_moves = [&](const State& s) {
        int i = get<0>(s);
        bool max_to_move = get<1>(s);
        long long max_score = get<2>(s);
        vector<State> moves;
        int remaining = n - i;
        if (remaining == 0) return moves;
        for (int take = 1; take <= 2 && take <= remaining; ++take) {
            long long taken = 0;
            for (int k = i; k < i + take; ++k) taken += coins[k];
            moves.push_back(State(i + take, !max_to_move, max_score + (max_to_move ? taken : 0)));
        }
        return moves;
    };

    function<double(const State&)> score = [&](const State& s) {
        return (double) get<2>(s);  // coins collected by the maximizing player at game end
    };

    pair<double, int> result = minimax<State>(State(0, true, 0), start, possible_moves, score);
    cout << (long long) result.first << " " << result.second << "\n";
    return 0;
}
