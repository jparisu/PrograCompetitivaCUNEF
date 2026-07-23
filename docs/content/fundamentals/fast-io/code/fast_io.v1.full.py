"""Fast I/O — read many integers quickly and print their sum.

Reading the whole input at once with `sys.stdin.buffer.read()` is much faster
than calling `input()` in a loop, which avoids Time Limit Exceeded on big cases.

Input:  an integer n, then n integers.
Output: the sum of the n integers.
"""
import sys


def main() -> None:
    data: list[bytes] = sys.stdin.buffer.read().split()
    n: int = int(data[0])
    total: int = sum(int(x) for x in data[1:1 + n])
    print(total)


main()
