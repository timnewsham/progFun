#!/usr/bin/env python3
#
# Code for showing how gaussian elimination works step by step.
#

class Eqn:
    def __init__(self, coeffs, rhs=[]):
        assert len(coeffs) > 0
        self.coeffs = coeffs
        self.rhs = rhs
    def cnt(self):
        return len(self.coeffs)
    def __str__(self):
        def param(var, n, coeef):
            if coeef == 0:
                return f"       "
            if coeef > 0:
                return f" {coeef:3.1f} {var}{n:d}"
            else:
                return f"{coeef:3.1f} {var}{n:d}"
        lhs = ' + '.join(param("x", n, coeff) for n, coeff in enumerate(self.coeffs))
        if self.rhs:
            rhs = ' + '.join(param("y", n, coeff) for n, coeff in enumerate(self.rhs))
        else:
            rhs = "..."
        return f'{lhs} = {rhs}'
    def sstr(self):
        # short string
        lhs = ' + '.join(f'{coeff:.1f} x{n}' for n, coeff in enumerate(self.coeffs) if self.coeffs)
        rhs = ' + '.join(f'{coeff:.1f} y{n}' for n, coeff in enumerate(self.coeffs) if self.rhs)
        return f'{lhs} = {rhs}'
    def scale(self, f):
        return Eqn([coeff * f for coeff in self.coeffs], [x * f for x in self.rhs])
    def copy(self):
        return Eqn(self.coeffs, self.rhs)
    def __add__(self, other):
        assert len(self.coeffs) == len(other.coeffs)
        coeffs = [vala + valb for vala, valb in zip(self.coeffs, other.coeffs)]
        rhs = [xa + xb for xa, xb in zip(self.rhs, other.rhs)]
        return Eqn(coeffs, rhs)
    def __sub__(self, other):
        return self + other.scale(-1)
    def apply(self, *vals):
        assert len(vals) == len(self.coeffs)
        return sum(val * coef for val, coef in zip(vals, self.coeffs))
    def apply_rhs(self, *vals):
        assert len(vals) == len(self.rhs)
        return sum(val * coef for val, coef in zip(vals, self.rhs))
    def verify(self, *vals):
        return self.apply(*vals) == self.apply_rhs(*vals)

class Eqns:
    def __init__(self, *eqns):
        assert len(eqns)
        self.eqn = list(eqns)
        assert all(eqns[0].cnt() == eqn.cnt() for eqn in eqns)
        for n in range(self.cnt()):
            self.eqn[n].rhs = [1 if n == m else 0 for m in range(self.cnt())]
    def cnt(self):
        return len(self.eqn)
    def __str__(self):
        return '\n'.join(f"{n}: {eqn}" for n,eqn in enumerate(self.eqn)) + "\n"
    def copy(self):
        eqns = [eqn.copy() for eqn in self.eqn]
        return Eqns(*eqns)
    def scale(self, n, f):
        self.eqn[n] = self.eqn[n].scale(f)

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

    def applies_lhs(self, *vals):
        return [eqn.apply(*vals) for eqn in self.eqn]
    def applies_rhs(self, *vals):
        return [eqn.apply_rhs(*vals) for eqn in self.eqn]

    def verify(self, lhs_vals, rhs_vals):
        print(f"see if transforming {lhs_vals} gives {rhs_vals}")
        for n, eqn in enumerate(self.eqn):
            lhs = eqn.apply(*lhs_vals)
            rhs = eqn.apply_rhs(*rhs_vals)
            ok = "ok" if approx_eq(rhs, lhs) else "wrong"
            print(f"{n}: {str(eqn):40s} | {lhs} == {rhs} {ok}")
        print()

def approx_eq(x, y):
    return abs(x - y) < 0.0001

example = Eqns(
    Eqn([2, 2, -3]),
    Eqn([1, 1,  1]),
    Eqn([2, 0,  2]),
)

def auto(orig):
    guess_lhs = [5 + n for n in range(orig.eqn[0].cnt())]
    guess_rhs = orig.applies_lhs(*guess_lhs)

    eqns = orig.copy()
    print("original problem to solve")
    print(eqns)
    eqns.verify(guess_lhs, guess_rhs)

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

    print("verify the inversion")
    eqns.verify(guess_lhs, guess_rhs)
    return eqns

if __name__ == '__main__':
    solved = auto(example)
    # solve example equation for [8,9,12], we should get [4,3,2]
    rhs = [8,9,2]
    lhs_soln = solved.applies_rhs(*rhs)
    print(f"solution is {lhs_soln} to get rhs == {rhs}")
    example.verify(lhs_soln, rhs)
    

