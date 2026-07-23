"""Loops demo — read n numbers and print their sum.

Illustrates a ``for`` loop with the accumulator pattern: a variable declared
outside the loop (``total``) is updated on every iteration. This is the building
block of almost every program: repeat some work a fixed number of times.

Input:
    An integer ``n``, then ``n`` integers (whitespace-separated).
Output:
    A single line with the sum of the ``n`` integers.
"""
import sys


def main() -> None:
    # Read every whitespace-separated token at once: data[0] is n, then n values.
    data: list[str] = sys.stdin.read().split()
    n: int = int(data[0])

    total: int = 0                  # accumulator for the running sum
    for i in range(1, n + 1):       # `for`: iterate over the n values (data[1..n])
        total += int(data[i])       # convert token to int and add it

    print(total)


main()
