#!/usr/bin/env python3

import time

def up_lines(n):
    print(f'\x1b[{n}A', end='')

def reverse(s):
    return f'\x1b[7m{s}\x1b[0m'

def seven_seg(a,b,c,d,e,f,g, REV=True):
    s = ' '
    on = reverse(' ') if REV else '#'
    off = '.'
    a = on if a else off
    b = on if b else off
    c = on if c else off
    d = on if d else off
    e = on if e else off
    f = on if f else off
    g = on if g else off
    return [
        f"{s}{a}{a}{a}{a}{a}{s}",
        f"{f}{s}{s}{s}{s}{s}{b}",
        f"{f}{s}{s}{s}{s}{s}{b}",
        f"{f}{s}{s}{s}{s}{s}{b}",
        f"{s}{g}{g}{g}{g}{g}{s}",
        f"{e}{s}{s}{s}{s}{s}{c}",
        f"{e}{s}{s}{s}{s}{s}{c}",
        f"{e}{s}{s}{s}{s}{s}{c}",
        f"{s}{d}{d}{d}{d}{d}{s}",
    ]

def seven_seg_decode(n, REV=True):
    if isinstance(n, str) and n in "0123456789":
        n = int(n)
    a = n in [0, 2, 3, 5, 6, 7, 8, 9]
    b = n in [0, 1, 2, 3, 4, 7, 8, 9]
    c = n in [0, 1, 3, 4, 5, 6, 7, 8, 9]
    d = n in [0, 2, 3, 5, 6, 8, 9]
    e = n in [0, 2, 6, 8]
    f = n in [0, 4, 5, 6, 8, 9]
    g = n in [2, 3, 4, 5, 6, 8, 9]
    return seven_seg(a,b,c,d,e,f,g, REV=REV)

def seven_seg_decodes(*ns, REV=True):
    segs = [seven_seg_decode(n, REV=REV) for n in ns]
    ls = ['  '.join(l) for l in zip(*segs)]
    return ls

def show(ls):
    for l in ls:
        print(l)

def test():
    #show(seven_seg_decodes(1,2,3))
    show(seven_seg_decodes('9','0','2','1','0', REV=False))
    show(seven_seg_decodes('9','0','2','1','0', REV=True))

def count():
    for nn in range(1000):
        if nn:
            up_lines(9)
        n = 999 - nn
        ns = [digit for digit in f'{n:3d}']
        show(seven_seg_decodes(*ns, REV=False))
        up_lines(9)
        time.sleep(0.05)
        show(seven_seg_decodes(*ns, REV=True))
        up_lines(9)
        time.sleep(0.05)
        show(seven_seg_decodes(*ns, REV=False))
        time.sleep(0.05)

if __name__ == '__main__':
    #test()
    count()
