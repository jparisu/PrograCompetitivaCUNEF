"""Minimax algorithm for two-player zero-sum games with perfect information.

Finds the optimal move for the player to move, assuming the opponent also plays
optimally: one player maximizes the score while the other minimizes it.

The algorithm is generic — it knows nothing about a specific game. A concrete
game only provides two functions and an initial state (see `test/driver.py` for
the Coins game used in the example):

- `possible_moves_funct(state)`: the list of states reachable from `state` in one
  move. An empty list means `state` is terminal (the game is over).
- `score_funct(state)`: the score of a terminal `state`, from the maximizing
  player's point of view (higher is better for them).

A *move* is identified by its index in the list returned by
`possible_moves_funct`, so `best_move` is the index of the chosen child.

Args:
    current_state: the current game state (any value the game functions accept).
    maximizing_player (int): +1 if the player to move maximizes, -1 if minimizes.
    possible_moves_funct (callable): state -> list of next states.
    score_funct (callable): terminal state -> float score.

Returns:
    tuple[float, int]: the optimal score, and the index of the best move
    (None if `current_state` is already terminal).
"""

def minimax(current_state, maximizing_player: int, possible_moves_funct, score_funct) -> tuple[float, int]:

    # Base case: a terminal state (no moves left) is scored directly.
    next_states = possible_moves_funct(current_state)
    if not next_states:
        return score_funct(current_state), None

    # The maximizing player wants the highest score, the minimizing one the lowest.
    best_value = float('-inf') if maximizing_player == 1 else float('inf')
    best_move = None

    # Try every move; the opponent moves next, so flip who is maximizing.
    for index, next_state in enumerate(next_states):
        value, _ = minimax(next_state, -maximizing_player, possible_moves_funct, score_funct)

        if maximizing_player == 1:
            if value > best_value:
                best_value, best_move = value, index
        else:
            if value < best_value:
                best_value, best_move = value, index

    return best_value, best_move
