#!/usr/bin/env python3

import time

def up_lines(n):
    print(f'\x1b[{n}A', end='')

def reverse(s):
    return f'\x1b[7m{s}\x1b[0m'

def seven_seg(a,b,c,d,e,f,g):
    s = ' '
    a = reverse(' ') if a else '.'
    b = reverse(' ') if b else '.'
    c = reverse(' ') if c else '.'
    d = reverse(' ') if d else '.'
    e = reverse(' ') if e else '.'
    f = reverse(' ') if f else '.'
    g = reverse(' ') if g else '.'
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

def seven_seg_decode(n):
    if n in "0123456789":
        n = int(n)
    a = n in [0, 2, 3, 5, 6, 7, 8, 9]
    b = n in [0, 1, 2, 3, 4, 7, 8, 9]
    c = n in [0, 1, 3, 4, 5, 6, 7, 8, 9]
    d = n in [0, 2, 3, 5, 6, 8, 9]
    e = n in [0, 2, 6, 8]
    f = n in [0, 4, 5, 6, 8, 9]
    g = n in [2, 3, 4, 5, 6, 8, 9]
    return seven_seg(a,b,c,d,e,f,g)

def seven_seg_decodes(*ns):
    segs = [seven_seg_decode(n) for n in ns]
    ls = ['  '.join(l) for l in zip(*segs)]
    return ls

def show(ls):
    for l in ls:
        print(l)

def test():
    #show(seven_seg_decode(5))
    show(seven_seg_decodes(9,0,2,1,0))

def count():
    for n in range(1000):
        if n:
            up_lines(9)
        ns = [digit for digit in f'{n:3d}']
        show(seven_seg_decodes(*ns))
        time.sleep(0.1)

if __name__ == '__main__':
    #test()
    count()
