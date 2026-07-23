# Python fast I/O — swap input() for the buffered reader (drop-in, at the top):
import sys
input = sys.stdin.readline
# input().split() reads one line; for many tokens at once: sys.stdin.read().split().
# Print a lot in one go:  print("\n".join(map(str, answers)))
