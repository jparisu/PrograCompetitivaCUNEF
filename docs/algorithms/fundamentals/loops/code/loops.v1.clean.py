# AUTO-GENERATED from loops.v1.full.py — do not edit.
# To override, replace this file with a hand-written version (remove this marker).
import sys
def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    total = 0
    for i in range(1, n + 1):
        total += int(data[i])
    print(total)
main()
