import sys
from impl import binary_search
d = sys.stdin.read().split()
n = int(d[0]); a = [int(x) for x in d[1:1 + n]]; t = int(d[1 + n])
print(binary_search(a, t))
