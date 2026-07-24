"""Coins game driver for the generic minimax.

Coins game: a row of coins is given; players alternate taking 1 or 2 coins from
the LEFT and keep their value. Both play optimally; the starting player wants to
maximize the coins they collect (zero-sum: the opponent minimizes them).

Protocol:
    line 1: the coin values, space-separated   (e.g. "2 3 5 8")
    line 2: the starting (maximizing) player    (e.g. "1")
Prints: "<best_value> <best_move>"  where best_move is 0 (take 1) or 1 (take 2).
"""
import sys
from impl import minimax


def main():
    lines = sys.stdin.read().splitlines()
    coins = [int(x) for x in lines[0].split()]
    start = int(lines[1]) if len(lines) > 1 and lines[1].strip() else 1
    n = len(coins)

    # State = (i, max_to_move, max_score): coins already taken from the left,
    # whether the maximizing (starting) player moves now, and how many coins that
    # player has collected so far.
    def possible_moves(state):
        i, max_to_move, max_score = state
        remaining = n - i
        if remaining == 0:
            return []
        moves = []
        for take in (1, 2):
            if take <= remaining:
                taken = sum(coins[i:i + take])
                moves.append((i + take, not max_to_move, max_score + (taken if max_to_move else 0)))
        return moves

    def score(state):
        return state[2]  # coins collected by the maximizing player at game end

    best_value, best_move = minimax((0, True, 0), start, possible_moves, score)
    print(f"{best_value} {best_move}")


main()
