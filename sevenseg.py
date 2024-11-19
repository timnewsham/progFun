#!/usr/bin/env python3

def maybe_print(ok, s):
    if ok:
        print(s, end='')

def seven_seg_line(n, a,b,c,d,e,f,g):
    s = ' '
    a = '=' if a else '.'
    b = '#' if b else '.'
    c = '#' if c else '.'
    d = '=' if d else '.'
    e = '#' if e else '.'
    f = '#' if f else '.'
    g = '=' if g else '.'
    maybe_print(n == 0, f"{s}{a}{a}{a}{a}{a}{s}")
    maybe_print(n == 1, f"{f}{s}{s}{s}{s}{s}{b}")
    maybe_print(n == 2, f"{f}{s}{s}{s}{s}{s}{b}")
    maybe_print(n == 3, f"{f}{s}{s}{s}{s}{s}{b}")
    maybe_print(n == 4, f"{s}{g}{g}{g}{g}{g}{s}")
    maybe_print(n == 5, f"{e}{s}{s}{s}{s}{s}{c}")
    maybe_print(n == 6, f"{e}{s}{s}{s}{s}{s}{c}")
    maybe_print(n == 7, f"{e}{s}{s}{s}{s}{s}{c}")
    maybe_print(n == 8, f"{s}{d}{d}{d}{d}{d}{s}")

def seven_seg_decode(l, n):
    a = n in [0, 2, 3, 5, 6, 7, 8, 9]
    b = n in [0, 1, 2, 3, 4, 7, 8, 9]
    c = n in [0, 1, 3, 4, 5, 6, 7, 8, 9]
    d = n in [0, 2, 3, 5, 6, 8, 9]
    e = n in [0, 2, 6, 8]
    f = n in [0, 4, 5, 6, 8, 9]
    g = n in [2, 3, 4, 5, 6, 8, 9]
    seven_seg_line(l, a,b,c,d,e,f,g)

def seven_segs(*ns):
    for l in range(9):
        for n in ns:
            seven_seg_decode(l, n)
            print("   ", end='')
        print()
    print()

seven_segs(0,1,2,3,4,5,6,7,8,9)
seven_segs(9,0,2,1,0)
