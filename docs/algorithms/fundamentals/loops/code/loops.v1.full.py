"""Loops demo — read n numbers and print their sum.

Shows the two basic loops (`for` and `while`), the building block of almost
every program: repeat some work a number of times or until a condition holds.

Input:
    An integer ``n``, then ``n`` integers (whitespace-separated).
Output:
    A single line with the sum of the ``n`` integers.
"""
import sys


def main() -> None:
    data: list[str] = sys.stdin.read().split()
    n: int = int(data[0])

    total: int = 0
    for i in range(1, n + 1):   # `for`: known number of repetitions
        total += int(data[i])

    print(total)


main()
