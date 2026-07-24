#! AUTO-GENERATED from minimax.v1.full.py — do not edit.
#! To override, replace this file with a hand-written version (remove this marker).
def minimax(current_state, maximizing_player: int, possible_moves_funct, score_funct) -> tuple[float, int]:

    next_states = possible_moves_funct(current_state)
    if not next_states:
        return score_funct(current_state), None

    best_value = float('-inf') if maximizing_player == 1 else float('inf')
    best_move = None

    for index, next_state in enumerate(next_states):
        value, _ = minimax(next_state, -maximizing_player, possible_moves_funct, score_funct)

        if maximizing_player == 1:
            if value > best_value:
                best_value, best_move = value, index
        else:
            if value < best_value:
                best_value, best_move = value, index

    return best_value, best_move
