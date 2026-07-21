"""Loops demo: read n numbers and print their sum.

Shows the two basic loops: `for` and `while`.
"""
import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])

    total = 0
    for i in range(1, n + 1):   # `for`: known number of repetitions
        total += int(data[i])

    print(total)


main()
