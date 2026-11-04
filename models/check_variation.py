"""Exact finite truthmaker variation. Standard-library only; run with Python 3."""
from itertools import product


def neg(a): return ('not', a)
def conj(a, b): return ('and', a, b)
def disj(a, b): return ('or', a, b)


class Model:
    def __init__(self, domains, atoms, worlds=None):
        self.worlds = tuple(product(*domains)) if worlds is None else tuple(worlds)
        self.atoms = atoms  # name -> (coordinate support, set of true worlds)
        self.cache = {}
        # Locality is an assumption of the import theorem, not of all H-C models.
        for support, truth in atoms.values():
            for u, v in product(self.worlds, repeat=2):
                if all(u[i] == v[i] for i in support):
                    assert (u in truth) == (v in truth), 'nonlocal atom'

    def makers(self, a, w):
        """Return (verifier supports, falsifier supports), with fusion preserved."""
        key = (a, w)
        if key in self.cache: return self.cache[key]
        if isinstance(a, str):
            support, truth = self.atoms[a]
            result = ({frozenset(support)}, set()) if w in truth else (set(), {frozenset(support)})
        elif a[0] == 'not':
            t, f = self.makers(a[1], w)
            result = f, t
        else:
            t1, f1 = self.makers(a[1], w)
            t2, f2 = self.makers(a[2], w)
            tf = {s | t for s in t1 for t in t2}
            ff = {s | t for s in f1 for t in f2}
            result = (tf, f1 | f2 | ff) if a[0] == 'and' else (t1 | t2 | tf, ff)
        self.cache[key] = result
        return result

    def select(self, w, a, centered=False):
        if centered and self.makers(a, w)[0]: return {w}
        return {v for v in self.worlds for s in self.makers(a, v)[0]
                if all(w[i] == v[i] for i in range(len(w)) if i not in s)}

    def relevant(self, a):
        if isinstance(a, str): return set(self.atoms[a][0])
        if a[0] == 'not': return self.relevant(a[1])
        return self.relevant(a[1]) | self.relevant(a[2])


def boolean_model():
    worlds = tuple(product((0, 1), repeat=2))
    return Model(((0, 1), (0, 1)), {
        'p': ({0}, {w for w in worlds if w[0]}),
        'q': ({1}, {w for w in worlds if w[1]}),
        'r': ({0, 1}, {w for w in worlds if w[0] != w[1]})})


def main():
    one = Model(((0, 1),), {'p': ({0}, {(1,)})})
    a, b, c, w = neg('p'), 'p', {(0,)}, (0,)
    assert one.select(w, disj(a, b), True) <= c
    assert not one.select(w, b, True) <= c
    print('Centered H-C SDA counterexample: disjunction {(0,)}, p {(1,)}')

    m = boolean_model()
    literals = ['p', 'q', 'r', neg('p'), neg('q'), neg('r')]
    formulas = literals + [op(a, b) for op in (conj, disj) for a, b in product(literals, repeat=2)]
    checked = separated = 0
    for w, a, b in product(m.worlds, formulas, formulas):
        ra, rb = m.select(w, a), m.select(w, b)
        joint = m.select(w, conj(a, b))
        sequential = set().union(*(m.select(u, b) for u in ra))
        assert joint <= sequential  # import
        assert ra | rb <= m.select(w, disj(a, b))  # SDA, inclusion not equality
        assert not m.makers(a, w)[0] or w in ra  # unrestricted MP
        if not m.relevant(a) & m.relevant(b):
            assert joint == sequential
            separated += 1
        checked += 1

    # Export fails even with satisfiable conjunction and non-tautological antecedents.
    a, b, w = 'p', disj(neg('p'), 'q'), (0, 0)
    joint = m.select(w, conj(a, b))
    seq = set().union(*(m.select(u, b) for u in m.select(w, a)))
    assert joint == {(1, 1)} and seq == {(0, 0), (0, 1), (1, 1)}
    assert joint <= m.atoms['p'][1] and not seq <= m.atoms['p'][1]

    # AS and equivalent-antecedent replacement fail; same witness, via absorption.
    w = (0, 0)
    assert m.select(w, 'p') <= m.atoms['r'][1]
    assert not m.select(w, conj('p', 'q')) <= m.atoms['r'][1]
    assert not m.select(w, disj('p', conj('p', 'q'))) <= m.atoms['r'][1]
    # CC fails despite MP: p∨¬p and r hold at (1,0), but (p∨¬p)>r fails.
    assert not m.select((1, 0), disj('p', neg('p'))) <= m.atoms['r'][1]
    # Here the true antecedent is the tautology p∨¬p, not the atom p.
    print(f'Checked {checked} ordered formula/world cases; {separated} disjoint-support cases.')
    print('Raw variation: SDA, MP, import verified; explicit AS, SEA, CC, export countermodels verified.')
    # Exact frame boundary: test every nonempty subset of the Boolean 3-cube.
    cube = tuple(product((0, 1), repeat=3))
    rectangular_count = 0
    for mask in range(1, 1 << len(cube)):
        points = {w for k, w in enumerate(cube) if mask & (1 << k)}
        atoms = {f'{i}={value}': ({i}, {w for w in points if w[i] == value})
                 for i in range(3) for value in (0, 1)}
        restricted = Model(((0, 1),) * 3, atoms, points)
        rectangular = points == set(product(*({w[i] for w in points} for i in range(3))))
        imports = True
        for w, v, i in product(points, points, range(3)):
            a = f'{i}={v[i]}'
            others = [f'{j}={v[j]}' for j in range(3) if j != i]
            b = conj(*others)
            joint = restricted.select(w, conj(a, b))
            seq = set().union(*(restricted.select(u, b) for u in restricted.select(w, a)))
            imports &= joint <= seq
        assert imports == rectangular
        rectangular_count += rectangular
    assert rectangular_count == 27
    print('All 255 nonempty Boolean 3-cube frames: import tests characterize exactly 27 rectangular frames.')
    print('These finite checks support, but do not replace, the accompanying general proofs.')


if __name__ == '__main__': main()
