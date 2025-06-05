#!/usr/bin/env python3
import sys

MAX = 256
def julia(x, c) :
    n = 0
    while n < MAX and abs(x) < 2.0 :
        n += 1
        x = x * x + c
    return n

def mand(c) :
    return julia(0, c)

W = 125
H = 39
CHARS = 'abcdefg'

def plot(x0, y0, x1, y1) :
    for yy in range(H) :
        y = y0 + (y1-y0) * yy / (H - 1)
        for xx in range(W) :
            x = x0 + (x1-x0) * xx / (W - 1)

            n = mand(complex(x, y))
            if n == MAX :
                ch = ' '
            else :
                ch = CHARS[n % len(CHARS)]
            sys.stdout.write(ch)
        sys.stdout.write('\n')
            
plot(-1.75, -1.1, 0.5, 1.1)
