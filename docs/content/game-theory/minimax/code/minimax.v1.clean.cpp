//! AUTO-GENERATED from minimax.v1.full.cpp — do not edit.
//! To override, replace this file with a hand-written version (remove this marker).
#include <vector>
#include <functional>
#include <limits>
#include <utility>
using namespace std;

template <typename State>
pair<double, int> minimax(
    const State& current_state,
    int maximizing_player,
    const function<vector<State>(const State&)>& possible_moves_funct,
    const function<double(const State&)>& score_funct) {

    vector<State> next_states = possible_moves_funct(current_state);
    if (next_states.empty())
        return {score_funct(current_state), -1};

    double best_value = (maximizing_player == 1)
        ? -numeric_limits<double>::infinity()
        :  numeric_limits<double>::infinity();
    int best_move = -1;

    for (int index = 0; index < (int) next_states.size(); ++index) {
        double value = minimax(next_states[index], -maximizing_player,
                               possible_moves_funct, score_funct).first;
        if (maximizing_player == 1) {
            if (value > best_value) { best_value = value; best_move = index; }
        } else {
            if (value < best_value) { best_value = value; best_move = index; }
        }
    }

    return {best_value, best_move};
}
