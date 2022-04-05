#!/usr/bin/env python3

import copy
import functools
import operator
import math

class Error(Exception):
    pass

CantSolve = Error("cant solve")

def sum(xs, unit=0):
    return functools.reduce(operator.add, xs, unit)

def prod(xs, unit=1):
    return functools.reduce(operator.mul, xs, unit)

def fact(n):
    return prod(range(1, n+1))

def permutations(xs, sgn):
    """
    permutations yields all permutions of xs.
    It also yields a positive sign if there were
    an even number of swaps, or a negative sign if
    there were an odd number of swaps.
    """
    if xs == []:
        yield [], sgn
        return
    for n,x in enumerate(xs):
        rest = xs[:n] + xs[n+1:]
        for perm,sgn2 in permutations(rest, sgn):
            yield [x] + perm, sgn2
        sgn *= -1.0

def sigma(n):
    """
    sigma yields all permutations of (0..n-1), along with
    a sign that is positive for an even number of swaps
    and negative for an odd number of swaps.
    """
    vs = list(range(n))
    return permutations(vs, 1.0)

def checkSigma():
    def check(n):
        perms = list(vs for vs,sgn in sigma(n))
        # we should have n! permutations
        assert len(perms) == fact(n)

        # each permutation should have values (0..n-1)
        for p in perms:
            assert all(m in p for m in range(n))

        # there should be no duplicates
        assert len(set(tuple(p) for p in perms)) == len(perms)
    check(3)
    check(4)
    check(5)
    check(6)

def ident(x):
    return x

def nop():
    return

def distr(op):
    #return op # XXX
    if op.typ != 'mul' or len(op.args) < 2:
        return op
    adds = [arg for arg in op.args if arg.typ == 'add']
    rest = [arg for arg in op.args if arg.typ != 'add']
    if len(adds) == 0:
        return op

    # distribute over the first add
    # (a+b) * c = a*c + b*c
    add,rest = adds[0], adds[1:] + rest
    #print("distributing", add, "over product of", rest)
    newrest = []
    for a in add.args:
        newrest.append(Sym.Mul(a, *rest))

    op = Sym.Add(*newrest)
    #print("distributed", add, "over", rest, "got", op)
    return op

def flatten(op):
    # flatten multiplies
    flat = []
    for a in op.args:
        if a.typ == op.typ:
            flat += list(a.args)
        else:
            flat.append(a)

    # reduce vals
    vals = []
    args = []
    for a in flat:
        if a.typ == "val":
            if a.val != op.unit:
                vals.append(a.val)
        else:
            args.append(a)
    if vals:
        val = op.reduce(vals)
        if val != op.unit:
            args[0:0] = [Sym.Val(val)]
    if len(args) == 0:
        return Sym.Val(op.unit)
    if len(args) == 1:
        return args[0]
    
    #op = copy.deepcopy(op)
    op.args = args
    return distr(op)

def gatherTerms(op, var):
    if op.typ != 'add':
        raise CantSolve

    def getTerm(op):
        if op.typ == 'val':
            return (0, op.val)
        if op.typ != 'mul':
            print(op)
            raise CantSolve
        vars = 0
        fac = 1
        for arg in op.args:
            if arg.typ == 'var':
                if arg.name == var:
                    vars += 1
                else:
                    raise CantSolve
            elif arg.typ == 'val':
                fac *= arg.val
            else:
                raise CantSolve
        return (vars, fac)

    terms = {}
    for arg in op.args:
        deg,fac = getTerm(arg)
        # simplifier isnt strong enough to gather like terms
        # so we do it here..
        if deg not in terms:
            terms[deg] = fac
        else:
            terms[deg] *= fac
    return terms

def quadraticRoots(a, b, c):
    """Solve a x^2 + b^x + c == 0 for x."""
    rad = b*b - 4*a*c
    if rad < 0:
        # no complex math here
        return CantSolve
    rad = math.sqrt(rad)
    return [(-b + rad) / 2*a,
            (-b - rad) / 2*a]

def linearRoots(b, c):
    """Solve b*x + c = 0 for x."""
    return [ -c/b ]

class Sym(object):
    def Var(nm):
        v = Sym("var")
        v.name = nm
        v.flatten = nop
        return v
    def Val(val):
        v = Sym("val")
        v.val = val
        v.flatten = nop
        return v
    def Add(*args):
        v = Sym("add")
        v.args = args
        v.reduce = sum
        v.unit = 0
        v.flatten = flatten
        return v.flatten(v)
    def Mul(*args):
        v = Sym("mul")
        v.args = args
        v.reduce = prod
        v.unit = 1
        v.flatten = flatten
        return v.flatten(v)
    def __init__(self, typ):
        self.typ = typ

    def roots(self, var):
        """Solve expr == 0 for var"""
        terms = gatherTerms(self, var)
        #print(terms)
        deg = max(deg for deg,fac in terms.items())
        if deg > 2:
            raise CantSolve
        a = terms.get(2, 0)
        b = terms.get(1, 0)
        c = terms.get(0, 0)
        if a:
            return quadraticRoots(a, b, c)
        # solve linear too?
        raise CantSolve

    def __mul__(a, b):
        return Sym.Mul(a, b)
    def __add__(a, b):
        return Sym.Add(a, b)
    def __repr__(self):
        if self.typ == "var":
            return self.name
        if self.typ == "val":
            return "%.f" % self.val
        if self.typ == "mul":
            return '(' + '*'.join(repr(a) for a in self.args) + ')'
        if self.typ == "add":
            return '(' + ' + '.join(repr(a) for a in self.args) + ')'

def Neg(x):
    return Sym.Mul(Sym.Val(-1), x)

def testSym():
    a = Sym.Var("a")
    b = Sym.Var("b")
    c = Sym.Var("c")
    d = Sym.Val(3)
    print(a * Sym.Val(2) * b * c * Sym.Val(4))
    print(a*b + c*d)

class Matrix(object):
    def FromVals(vals):
        m = len(vals)
        n = len(vals[0])
        m = Matrix(n, m)
        m.set(vals)
        return m
    def Vec(*vals):
        return Matrix.FromVals([[x] for x in vals])

    def __init__(self, n, m):
        self.n = n # rows
        self.m = m # cols
        # indexed as vals[col][row]
        self.vals = [[0]*n for _ in range(m)]


    def set(self, vals):
        assert len(vals) == self.m
        assert all(len(row) == self.n for row in vals)
        self.vals = copy.deepcopy(vals)

    def __repr__(self):
        strs = [
            [str(row) for row in col]
            for col in self.vals
        ]
        widths = [
            max(len(strs[m][n]) for m in range(self.m))
            for n in range(self.n)
        ]
        for m in range(self.m):
            for n in range(self.n):
                w = widths[n] 
                curw = len(strs[m][n])
                strs[m][n] = ' ' * (w-curw) + strs[m][n]

        s = '\n'.join(
            '| ' + '  '.join(row for row in col) + ' |'
            for col in strs) + '\n'
        return s

    def transpose(self):
        new = Matrix(self.m, self.n)
        for m,row in enumerate(self.vals):
            for n,x in enumerate(row):
                new.vals[n][m] = x
        return new 

    def mult(a, b):
        assert a.n == b.m
        c = Matrix(a.m, b.n)
        for m in range(c.m):
            for n in range(c.n):
                c.vals[m][n] = sum(a.vals[m][p] * b.vals[p][n] for p in range(a.n))
        return c
        
    def dot(a, b):
        return a.transpose().mult(b)

    def det(a, const=ident):
        # Leibniz formula
        # see https://en.wikipedia.org/wiki/Determinant#n_%C3%97_n_matrices
        assert a.n == a.m
        return sum((
            const(sgn) * prod((a.vals[i][sig[i]] for i in range(a.n)), const(1))
            for sig,sgn in sigma(a.n)), const(0))
            
            

def test():
    vs = [[1, 0, 0],
        [1, 1, 0],
        [0, 0, 1]]
    vs = [[1, 0, 99],
        [1, 1, 0]]
    m = Matrix.FromVals(vs)
    print(m)
    print(m.transpose())
    
    
    v = Matrix.Vec(1,2,3)
    v2 = v.transpose()
    print(v)
    print(v2)
    print(v2.mult(v)) # 14
    assert v2.mult(v).vals[0][0] == 14
    
    print(v.dot(v)) # 14
    assert v.dot(v).vals[0][0] == 14

    print(Matrix.Vec(1,2,3).dot(Matrix.Vec(2,2,2))) # 12
    assert Matrix.Vec(1,2,3).dot(Matrix.Vec(2,2,2)).vals[0][0] == 12
    
    checkSigma()
    
    m = Matrix.FromVals([
        [6, 4],
        [3, 5]])
    print(m)
    print(m.det()) # 18
    assert m.det() == 18

    m = Matrix.FromVals([
        [1,3,2],
        [-3, -1, -3],
        [2,3,1]])
    print(m.det()) # -15
    assert m.det() == -15

    """
    m = Matrix.FromVals([
        [Sym.Val(2) + Neg(Sym.Var('a')), Sym.Var('b')],
        [Sym.Var('c'), Sym.Val(3) + Neg(Sym.Var('d'))],
    ])
    """
    m = Matrix.FromVals([
        [Sym.Val(2) + Neg(Sym.Var('L')), Sym.Val(8)],
        [Sym.Val(7), Sym.Val(3) + Neg(Sym.Var('L'))],
    ])
    print("compute symbolic determinant")
    print(m)
    det = m.det(const=Sym.Val)
    print("determinant", det)
    print("roots", det.roots('L'))


test()
#testSym()
