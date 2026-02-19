#!/usr/bin/env python3
import sys
"""
Cellular automata.
"""
import random

def bits(n, sz):
    """Convert a number into a bit string of size sz."""
    #return [(n >> sh) & 1 for sh in range(sz)]
    return [(n // 2**p) % 2 for p in range(sz)]

def unbits(bs):
    #return sum(b << sh for sh,b in enumerate(bs))
    return sum(bs[n] * (2**n) for n in range(len(bs)))

def seed(sz):
    """Return a vector of length sz whose elements are all zero except the middle one."""
    return [1 if n == (sz//2) else 0 for n in range(sz)]

def rseed(sz):
    """Return a vector of length sz whose elements are chosen from random."""
    return [random.choice([0,1]) for n in range(sz)]

def next_val(rulev, neigh):
    """Return the next value given neighbors [a,b,c] using rulevector"""
    return rulev[unbits(neigh)]

def get(v, n):
    """Get the value in v[] at n, wrapping around when necessary."""
    return v[n % len(v)]

def neighborhood(v, n):
    """Return the neighborhood around n."""
    return [get(v, n-1), get(v, n), get(v, n+1)]

def evolve(rulev, v):
    """compute each new value from the neighbors of each current value."""
    return [next_val(rulev, neighborhood(v, n)) for n in range(len(v))]

def show(vec):
    return ''.join('*' if v else ' ' for v in vec)

def show_rule(rulev):
    """Print out the rule in human readable form."""
    for n in range(8):
        inp = bits(n, 3)
        outp = bits(rulev[n], 1)
        print(f"[{show(inp)}] -> [{show(outp)}]")
    print()

def run(rule, sz, seedfunc=seed):
    """Run the evolution of a seed using the rule."""
    # each rule number from zero to 256 makes a rulevector of size 8.
    assert 0 <= rule and rule < 256
    rulev = bits(rule, 8)
    show_rule(rulev)

    # start with a single seed value and 
    # run forever while evolving using the rule vector
    v = seedfunc(sz)
    while True:
        print(show(v))
        v = evolve(rulev, v)

# interesting rules: 90, 110, 193
def main():
    size = 75 
    rule = 90
    s = seed
    if len(sys.argv) > 1:
        rule = int(sys.argv[1])
    if len(sys.argv) > 2:
        size = int(sys.argv[2])
    if len(sys.argv) > 3 and sys.argv[3][0] == 'r':
        s = rseed
    print(f"rule {rule}, size {size}")

    run(rule, size, s)

if __name__ == '__main__':
    main()
