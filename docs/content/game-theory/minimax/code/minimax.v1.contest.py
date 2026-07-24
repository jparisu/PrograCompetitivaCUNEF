#! AUTO-GENERATED from minimax.v1.clean.py — do not edit.
#! To override, replace this file with a hand-written version (remove this marker).
def minimax(c, e, h, i):
    g = h(c)
    if not g:
        return (i(c), None)
    b = float('-inf') if e == 1 else float('inf')
    a = None
    for d, f in enumerate(g):
        j, _ = minimax(f, -e, h, i)
        if e == 1:
            if j > b:
                b, a = (j, d)
        elif j < b:
            b, a = (j, d)
    return (b, a)
