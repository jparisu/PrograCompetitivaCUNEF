# AUTO-GENERATED from loops.v1.clean.py — do not edit.
# To override, replace this file with a hand-written version (remove this marker).
import sys

def main():
    a = sys.stdin.read().split()
    c = int(a[0])
    d = 0
    for b in range(1, c + 1):
        d += int(a[b])
    print(d)
main()
