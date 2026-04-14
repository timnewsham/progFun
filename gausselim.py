#!/usr/bin/env python3
#
# Code for showing how gaussian elimination works step by step.
#

class Eqn:
    def __init__(self, coeffs, eq):
        assert len(coeffs) > 0
        self.coeffs = coeffs
        self.eq = eq
    def cnt(self):
        return len(self.coeffs)
    def __str__(self):
        def param(n, coeef):
            if coeef == 0:
                return f"       "
            if coeef > 0:
                return f" {coeef:3.1f} x{n:d}"
            else:
                return f"{coeef:3.1f} x{n:d}"
        lhs = ' + '.join(param(n, coeff) for n, coeff in enumerate(self.coeffs))
        return f'{lhs} = {self.eq:.1f}'
    def sstr(self):
        # short string
        lhs = ' + '.join(f'{coeff:.1f} x{n}' for n, coeff in enumerate(self.coeffs) if coeff)
        return f'{lhs} = {self.eq:.1f}'
    def scale(self, f):
        return Eqn([coeff * f for coeff in self.coeffs], self.eq * f)
    def copy(self):
        return Eqn(self.coeffs, self.eq)
    def __add__(self, other):
        assert len(self.coeffs) == len(other.coeffs)
        vals = [vala + valb for vala, valb in zip(self.coeffs, other.coeffs)]
        return Eqn([ca + cb for ca, cb in zip(self.coeffs, other.coeffs)], self.eq + other.eq)
    def __sub__(self, other):
        return self + other.scale(-1)
    def apply(self, *vals):
        assert len(vals) == len(self.coeffs)
        return sum(val * coef for val, coef in zip(vals, self.coeffs))
    def verify(self, *vals):
        return self.apply(*vals) == self.eq

class Eqns:
    def __init__(self, *eqns):
        assert len(eqns)
        assert all(eqns[0].cnt() == eqn.cnt() for eqn in eqns)
        self.eqn = list(eqns)
    def cnt(self):
        return len(self.eqn)
    def __str__(self):
        return '\n'.join(f"{n}: {eqn}" for n,eqn in enumerate(self.eqn)) + "\n"
    def copy(self):
        eqns = [eqn.copy() for eqn in self.eqn]
        return Eqns(*eqns)
    def scale(self, n, f):
        self.eqn[n] = self.eqn[n].scale(f)
    def rhs(self):
        return [eqn.eq for eqn in self.eqn]

    def swap(self, a, b):
        print(f"swap equations {a} and {b}")
        self.eqn[a], self.eqn[b] = self.eqn[b], self.eqn[a]
        print(self)

    def can_norm(self, n, pos):
        val = self.eqn[n].coeffs[pos]
        if val == 0:
            print(f"cant normalize equation {n} at position {pos} because its coefficient is zero there")
        return val != 0

    def norm(self, n, pos):
        f = 1.0 / self.eqn[n].coeffs[n]
        print(f"replace equation {n} with {f}*({self.eqn[n].sstr()})")
        self.eqn[n] = self.eqn[n].scale(f)
        print(self)

    def elim(self, n, pos):
        # self.eqn[pos][pos] should be 1.0 or very close to it due to normalization.
        f = self.eqn[n].coeffs[pos]
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
    Eqn([2, 2, -3],  8),
    Eqn([1, 1,  1],  9),
    Eqn([2, 0,  2], 12),
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

def auto(orig):
    eqns = orig.copy()
    print("original problem to solve")
    print(eqns)

    # take care of the lower triangle
    for n in range(eqns.cnt()):
        print(f"work on column {n}")
        # we want to normalize position n
        # find an equation that is normalizable at that position, swapping if necessary
        for m in range(n, eqns.cnt()):
            if eqns.can_norm(m, n):
                break
        else:
            raise Error("impossible to solve")
        if m != n:
            eqns.swap(n, m)

        # now we can normalize equation n at position n
        assert eqns.can_norm(n, n)
        print(f"we can normalize equation {n} at position {n}")
        eqns.norm(n, n)

        # we want to eliminate at pos n for all following equations
        for m in range(n + 1, eqns.cnt()):
            eqns.elim(m, n)

    # take care of the upper triangle
    for n in range(eqns.cnt()-1, -1, -1):
        for m in range(n-1, -1, -1):
            eqns.elim(m, n)

    sln = eqns.rhs()
    print(f"the answer is {sln}")
    print()

    print("verify our original equations")
    orig.verify(*sln)

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
    print()

    print("verify our current equations")
    eqns.verify(*sln)
    print("verify our original equations")
    example.verify(*sln)


if __name__ == '__main__':
    print("tests ---------------")
    test()
    print()

    print("solving example ---------------")
    solve()
    print()

    print("auto solution ---------------")
    auto(example)
