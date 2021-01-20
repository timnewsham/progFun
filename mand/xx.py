#!/usr/bin/env python
import math
def j(x,c,n=256):
 while n>0 and abs(x)<=2.0:n,x=n-1,x*x+c
 return n
w,h=10,10
def p(f,x,y,u,v,c=' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY'):
 return '\n'.join(''.join(c[f(x,y)%len(c)] for x in [x+m*(u-x)/(w-1) for m in xrange(w)]) for y in [y+m*(v-y)/(h-1) for m in xrange(h)])
def floor(x) :
    if x < 0 :
        return -math.floor(-x)
    return math.floor(x)
def moire(x,y) :
    m = int(x*y) % 3
    print x,y, x*y, int(x*y), m
    return m
print p(moire,-8.0,-8.0,8.0,8.0)
