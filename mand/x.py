def j(x,c,n=256): 
 while n>0 and abs(x)<=2.0:n,x=n-1,x*x+c
 return n
def p(f,x,y,u,v,w=125,h=39,c=' abcdefg'): return '\n'.join(''.join(c[f(x+m*(u-x)/(w-1),y+n*(v-y)/(h-1))%len(c)] for m in xrange(w)) for n in xrange(h))
print '%s\n\n%s\n\n%s'%(p(lambda x,y:j(0,complex(x,y)),-1.75,-1.1,0.5,1.1),p(lambda x,y:j(complex(x,y),0.3+0.5j),-1.5,-1.5,1.5,1.5),p(lambda x,y:int(x*y)%3,-8.0,-8.0,8.0,8.0))
