#!/usr/bin/env python
I,L,S,T = isinstance,list,str,tuple
def t(i,x) :
 x=e(x)
 print '%s: %s'%(i,x) 
 return x
def b(x):return [('x',('y', 'x')), ('x',('y', 'y'))][int(x)]
bs={'add':lambda x,y:e(x)+e(y),'mod':lambda x,y:e(x)%e(y),'eq':lambda x,y:b(e(x)==e(y)),'lt':lambda x,y:b(e(x)<e(y)),'seq':lambda x,y:[e(x),y][1],'trace':t}
def ex(bd,vr,vl):
 if I(bd,L):return [ex(x,vr,vl) for x in bd]
 elif I(bd,S) and bd==vr:return vl
 elif I(bd,T) and bd[0]!=vr:return bd[0],ex(bd[1],vr,vl)
 else:return bd
def ap(f,a) :
 if I(f,T):return ex(f[1],f[0],a)
 if I(f,S):return (lambda x:lambda y:bs[f](x,y))(a)
 return f(a)
def e(x) :
 if not I(x,L):return x
 f=e(x[0])
 for a in x[1:]:f=e(ap(f,a))
 return e(f)
ref1=('l',[('c',[('j',[('o',[('k',[('r',[('s',[('q',['s','prime',['r',10,'q']]),['o',('x',('y',['eq',['mod','y','x'],0])),['k',['add',1],2]]]),[('f',[('x',['f',['x','x']]),('x',['f',['x','x']])]),('s',('id',('xs',['xs','d',('y',('ys',['seq',['trace','id','y'],['s','id','ys']]))])))]]),[('f',[('x',['f',['x','x']]),('x',['f',['x','x']])]),('r',('n',('xs',['if',['eq','n',0],'l',['xs','l',('y',('ys',['c','y',['r',['add','n',-1],'ys']]))]])))]]),[('f',[('x',['f',['x','x']]),('x',['f',['x','x']])]),('k',('f',('x0',['c','x0',['k','f',['f','x0']]])))]]),[('f',[('x',['f',['x','x']]),('x',['f',['x','x']])]),('o',('f',('xs',['xs','l',('y',('ys',['c','y',['o','f',['j',['h','m',['f','y']],'ys']]]))])))]]),[('f',[('x',['f',['x','x']]),('x',['f',['x','x']])]),('j',('p',('xs',['xs','l',('y',('ys',['if',['p','y'],['c','y',['j','p','ys']],['j','p','ys']]))])))]]),('x',('xs',('f',('g',['g','x','xs']))))])
e([('h',[('i',[('u',[('if',[('m',[ref1,('f',('g','f'))]),('b',['b','u','i'])]),('b',('t',('e',['b','e','t'])))]),('x',('y','y'))]),('x',('y','x'))]),('f',('g',('x',['f',['g','x']])))])
