import sys

data = sys.stdin.buffer.read().split()   # fast input: read all tokens at once
it = iter(data)
def read_int():                          # next integer from the input
    return int(next(it))

out = sys.stdout.write                   # fast output: out(str(x) + "\n")
