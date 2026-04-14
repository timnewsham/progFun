#!/usr/bin/env python3
#
# Code for showing how gaussian elimination works step by step.
#

class Eqn:
    def __init__(self, *vals):
        assert len(vals) > 1
        self.vals = vals
    def cnt(self):
        return len(self.vals) - 1
    def __str__(self):
        def param(n, coeef):
            if coeef == 0:
                return f"       "
            if coeef > 0:
                return f" {coeef:3.1f} x{n:d}"
            else:
                return f"{coeef:3.1f} x{n:d}"
        coefs = self.vals[:-1]
        eq = self.vals[-1]
        lhs = ' + '.join(param(n, coeff) for n, coeff in enumerate(coefs))
        rhs = f"{eq:.2f}"
        return f'{lhs} = {eq:.1f}'
    def sstr(self):
        # short string
        coefs = self.vals[:-1]
        eq = self.vals[-1]
        lhs = ' + '.join(f'{coeff:.1f} x{n}' for n, coeff in enumerate(coefs) if coeff)
        rhs = f"{eq:.2f}"
        return f'{lhs} = {eq:.1f}'
    def scale(self, f):
        return Eqn(*[val * f for val in self.vals])
    def copy(self):
        return Eqn(*self.vals)
    def __add__(self, other):
        assert len(self.vals) == len(other.vals)
        vals = [vala + valb for vala, valb in zip(self.vals, other.vals)]
        return Eqn(*vals)
    def __sub__(self, other):
        return self + other.scale(-1)
    def apply(self, *vals):
        coefs = self.vals[:-1]
        assert len(vals) == len(coefs)
        return sum(val * coef for val, coef in zip(vals, coefs))
    def verify(self, *vals):
        eq = self.vals[-1]
        return self.apply(*vals) == eq

class Eqns:
    def __init__(self, *eqns):
        assert len(eqns)
        assert all(eqns[0].cnt() == eqn.cnt() for eqn in eqns)
        self.eqn = list(eqns)
    def copy(self):
        eqns = [eqn.copy() for eqn in self.eqn]
        return Eqns(*eqns)
    def __str__(self):
        return '\n'.join(f"{n}: {eqn}" for n,eqn in enumerate(self.eqn)) + "\n"
    def scale(self, n, f):
        self.eqn[n] = self.eqn[n].scale(f)
    def rhs(self):
        return [eqn.vals[-1] for eqn in self.eqn]

    def swap(self, a, b):
        print(f"swap equations {a} and {b}")
        self.eqn[a], self.eqn[b] = self.eqn[b], self.eqn[a]
        print(self)

    def norm(self, n, pos):
        f = 1.0 / self.eqn[n].vals[n]
        print(f"replace equation {n} with {f}*({self.eqn[n].sstr()})")
        self.eqn[n] = self.eqn[n].scale(f)
        print(self)

    def elim(self, n, pos):
        # self.eqn[pos][pos] should be 1.0 or very close to it due to normalization.
        f = self.eqn[n].vals[pos]
        print(f"replace equation {n} with ({self.eqn[n].sstr()}) - {f}*({self.eqn[pos].sstr()})")
        self.eqn[n] = self.eqn[n] - self.eqn[pos].scale(f)
        print(self)

    def verify(self, *vals):
        for n, eqn in enumerate(self.eqn):
            e = eqn.apply(*vals)
            ok = "ok" if eqn.verify(*vals) else "wrong"
            print(f"{n}: {str(eqn):40s} | evaluated to {e}, {ok}")
        print()
        

example = Eqns(
    Eqn(2, 2, -3,  8),
    Eqn(1, 1,  1,  9),
    Eqn(2, 0,  2, 12),
)

def test():
    eqns = example
    print(eqns)
    print(eqns.swap(0, 1))

    print("eq0 + eq1", eqns.eqn[0] + eqns.eqn[1])
    print("eq1 - eq0", eqns.eqn[1] - eqns.eqn[0])
    print()

    print("eval for x0,x1,x2 = 4,3,2")
    eqns.verify(4,3,2,)

def solve():
    eqns = example.copy()
    print("original problem to solve")
    print(eqns)

    # take care of lower triangle
    eqns.norm(0, 0)
    eqns.elim(1, 0)
    eqns.elim(2, 0)
    eqns.swap(1, 2)
    eqns.norm(1, 1)
    eqns.elim(2, 1)
    eqns.norm(2, 2)

    # take care of upper triangle
    eqns.elim(1, 2)
    eqns.elim(0, 2)
    eqns.elim(0, 1)
    sln = eqns.rhs()
    print(f"the answer is {sln}")

    print("verify our current equations")
    eqns.verify(*sln)
    print("verify our original equations")
    example.verify(*sln)


if __name__ == '__main__':
    #test()
    solve()
