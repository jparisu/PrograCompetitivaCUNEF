/**
 * Minimax algorithm for two-player zero-sum games with perfect information.
 *
 * Finds the optimal move for the player to move, assuming the opponent also
 * plays optimally: one player maximizes the score, the other minimizes it.
 *
 * The algorithm is generic. A concrete game (see test/driver.cpp for the Coins
 * game) provides its own State type and two functions:
 *   - possible_moves_funct(state): the states reachable in one move; an empty
 *     vector means `state` is terminal (the game is over).
 *   - score_funct(state): the score of a terminal state, from the maximizing
 *     player's point of view (higher is better for them).
 *
 * A move is identified by its index in the possible_moves list, so best_move is
 * the index of the chosen child (-1 if `current_state` is already terminal).
 *
 * Returns: {best_value, best_move}.
 * Complexity: O(b^d) time, O(d) space (b = branching factor, d = tree depth).
 */
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

    // Base case: a terminal state (no moves left) is scored directly.
    vector<State> next_states = possible_moves_funct(current_state);
    if (next_states.empty())
        return {score_funct(current_state), -1};

    // The maximizing player wants the highest score, the minimizing one the lowest.
    double best_value = (maximizing_player == 1)
        ? -numeric_limits<double>::infinity()
        :  numeric_limits<double>::infinity();
    int best_move = -1;

    // Try every move; the opponent moves next, so flip who is maximizing.
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
