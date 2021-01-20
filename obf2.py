#!/usr/bin/env python
def t(i,x):x=e(x);print i,x;return x
def F(b,r,l):
 if I(b,L):return[F(x,r,l)for x in b]
 if I(b,S)and b==r:return l
 if I(b,T)and b[0]!=r:return b[0],F(b[1],r,l)
 return b
def G(f,a):
 if I(f,T):return F(f[1],f[0],a)
 if I(f,S):return(lambda x:lambda y:{A:lambda x,y:e(x)+e(y),M:lambda x,y:e(x)%e(y),E:lambda x,y:[(l,(c,l)),(l,(c,c))][int((e(x)==e(y)))],V:lambda x,y:[e(x),y][1],U:t}[f](x,y))(a)
 return f(a)
def e(x):
 if I(x,L):return e(reduce(lambda f,a:e(G(f,a)),x[1:],e(x[0])))
 return x
I,L,S,T=isinstance,list,str,tuple;l,c,j,o,k,r,s,q,x,y,f,d,n,p,g,h,m,B,u,i,Z,Y,A,E,M,U,V,J,X,W,C,K=map(S,range(64,96));H=(l,[(c,[(j,[(o,[(k,[(r,[(s,[(q,[s,'prime',[r,15,q]]),[o,(x,(y,[E,[M,y,x],0])),[k,[A,1],2]]]),[(f,[(x,[f,[x,x]]),(x,[f,[x,x]])]),(s,(J,(X,[X,d,(y,(W,[V,[U,J,y],[s,J,W]]))])))]]),[(f,[(x,[f,[x,x]]),(x,[f,[x,x]])]),(r,(n,(X,[K,[E,n,0],l,[X,l,(y,(W,[c,y,[r,[A,n,-1],W]]))]])))]]),[(f,[(x,[f,[x,x]]),(x,[f,[x,x]])]),(k,(f,(C,[c,C,[k,f,[f,C]]])))]]),[(f,[(x,[f,[x,x]]),(x,[f,[x,x]])]),(o,(f,(X,[X,l,(y,(W,[c,y,[o,f,[j,[h,m,[f,y]],W]]]))])))]]),[(f,[(x,[f,[x,x]]),(x,[f,[x,x]])]),(j,(p,(X,[X,l,(y,(W,[K,[p,y],[c,y,[j,p,W]],[j,p,W]]))])))]]),(x,(X,(f,(g,[g,x,X]))))]);e([(h,[(i,[(u,[(K,[(m,[H,(f,(g,f))]),(B,[B,u,i])]),(B,(Z,(Y,[B,Y,Z])))]),(x,(y,y))]),(x,(y,x))]),(f,(g,(x,[f,[g,x]])))])
