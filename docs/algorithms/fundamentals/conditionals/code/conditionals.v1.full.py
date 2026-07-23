"""Conditionals demo — print the larger of two numbers.

Shows `if` / `else`: choosing what to do based on a condition.

Input:  two integers a and b.
Output: the larger of the two.
"""
import sys


def main() -> None:
    data: list[str] = sys.stdin.read().split()
    a: int = int(data[0])
    b: int = int(data[1])
    if a > b:
        print(a)
    else:
        print(b)


main()
