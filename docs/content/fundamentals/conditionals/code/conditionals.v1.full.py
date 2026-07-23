"""Conditionals demo — print the larger of two numbers.

Shows `if` / `else`: choosing what to do based on a condition.

Input:  two integers a and b (separated by whitespace).
Output: the larger of the two (or either one when they are equal).
"""
import sys


def main() -> None:
    # Read the whole input and split on any whitespace into tokens.
    data: list[str] = sys.stdin.read().split()
    a: int = int(data[0])
    b: int = int(data[1])

    # The branch that runs is decided at run time from the comparison.
    # (`a >= b` would also be correct: on a tie we may print either one.)
    if a > b:
        print(a)
    else:
        print(b)


main()
