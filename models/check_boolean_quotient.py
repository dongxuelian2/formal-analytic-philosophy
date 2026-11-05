"""Independent finite checks of the visible Boolean quotient theorem.

Standard library only. Raw endpoints use per-world bilateral support
recursion; the comparison uses visible partial assignments, not raw paths.
Finite checks support the written proof and make no novelty claim.
"""
from functools import lru_cache
from itertools import product
import random


@lru_cache(None)
def assignments(a, sign=True):
    if isinstance(a, int):
        return frozenset((frozenset(((a, int(sign)),)),))
    if a[0] == 'not':
        return assignments(a[1], not sign)
    left, right = assignments(a[1], sign), assignments(a[2], sign)
    fused = set()
    for u in left:
        for v in right:
            if all(p != q or b == c for p, b in u for q, c in v):
                fused.add(u | v)
    conjunctive = (a[0] == 'and') == sign
    return frozenset(fused) if conjunctive else left | right | frozenset(fused)


def overwrite(w, u):
    result = list(w)
    for p, bit in u:
        result[p] = bit
    return tuple(result)


class Raw:
    def __init__(self, worlds, supports, values):
        self.worlds = tuple(worlds)
        self.supports = supports
        self.values = values
        self.n = len(supports)

    def same_outside(self, w, v, support):
        return all(i in support or a == b for i, (a, b) in enumerate(zip(w, v)))

    @lru_cache(None)
    def makers(self, a, w):
        if isinstance(a, int):
            one, zero = frozenset((self.supports[a],)), frozenset()
            return (one, zero) if self.values[w][a] else (zero, one)
        if a[0] == 'not':
            pos, neg = self.makers(a[1], w)
            return neg, pos
        pos1, neg1 = self.makers(a[1], w)
        pos2, neg2 = self.makers(a[2], w)
        fp = frozenset(s | t for s in pos1 for t in pos2)
        fn = frozenset(s | t for s in neg1 for t in neg2)
        return ((fp, neg1 | neg2 | fn) if a[0] == 'and'
                else (pos1 | pos2 | fp, fn))

    @lru_cache(None)
    def successors(self, a, w):
        return frozenset(v for v in self.worlds
                         if any(self.same_outside(w, v, s)
                                for s in self.makers(a, v)[0]))

    def criteria(self):
        for p in range(self.n):
            for w in self.worlds:
                reset = [v for v in self.worlds
                         if self.same_outside(w, v, self.supports[p])]
                if {self.values[v][p] for v in reset} != {0, 1}:
                    return False
                if any(self.values[v][q] != self.values[w][q]
                       for v in reset for q in range(self.n) if q != p):
                    return False
        return True

    def clear(self):
        self.makers.cache_clear()
        self.successors.cache_clear()


def evaluate(phi, w, values, successors):
    if isinstance(phi, int):
        return bool(values(w)[phi])
    if phi[0] == 'not':
        return not evaluate(phi[1], w, values, successors)
    if phi[0] == 'and':
        return (evaluate(phi[1], w, values, successors)
                and evaluate(phi[2], w, values, successors))
    if phi[0] == 'or':
        return (evaluate(phi[1], w, values, successors)
                or evaluate(phi[2], w, values, successors))
    return all(evaluate(phi[2], v, values, successors)
               for v in successors(phi[1], w))


def cube_successors(a, w):
    return {overwrite(w, u) for u in assignments(a)}


def formulas(n):
    rng = random.Random(508)
    literals = [p for p in range(n)] + [('not', p) for p in range(n)]
    fixed = literals + [(op, a, b) for op in ('and', 'or')
                        for a in literals for b in literals]

    def normal(depth):
        if not depth or rng.random() < .25:
            return rng.choice(literals)
        op = rng.choice(('and', 'or', 'not'))
        return ((op, normal(depth - 1)) if op == 'not'
                else (op, normal(depth - 1), normal(depth - 1)))

    normal_forms = tuple(dict.fromkeys(fixed + [normal(3) for _ in range(30)]))
    nested = [('box', normal(2), ('box', normal(2), normal(2)))
              for _ in range(20)]
    nested += [('not', ('box', normal(2), ('not', normal(2))))
               for _ in range(10)]
    return normal_forms, nested


def check_model(model):
    assert model.criteria()
    assert set(model.values.values()) == set(product((0, 1), repeat=model.n))
    normal, nested = formulas(model.n)
    endpoint_count = nested_count = 0
    for a in normal:
        for w in model.worlds:
            actual = {model.values[v] for v in model.successors(a, w)}
            assert actual == cube_successors(a, model.values[w]), (a, w)
            endpoint_count += 1
    for phi in nested:
        for w in model.worlds:
            assert evaluate(phi, w, model.values.__getitem__, model.successors) == \
                evaluate(phi, model.values[w], lambda v: v, cube_successors)
            nested_count += 1
    model.clear()
    return endpoint_count, nested_count


def local_atoms(worlds, ncoords):
    options = []
    for mask in range(1 << ncoords):
        support = frozenset(i for i in range(ncoords) if mask >> i & 1)
        patterns = tuple(dict.fromkeys(tuple(w[i] for i in sorted(support))
                                       for w in worlds))
        for bits in product((0, 1), repeat=len(patterns)):
            table = dict(zip(patterns, bits))
            values = tuple(table[tuple(w[i] for i in sorted(support))] for w in worlds)
            options.append((support, values))
    return options


def main():
    atomic_cases = valid_models = endpoints = nested = 0
    for ncoords in (1, 2, 3):
        worlds = tuple(product((0, 1), repeat=ncoords))
        options = local_atoms(worlds, ncoords)
        # First test every local two-atom input, including failed criteria.
        for (sp, vp), (sq, vq) in product(options, repeat=2):
            values = dict(zip(worlds, zip(vp, vq)))
            model = Raw(worlds, (sp, sq), values)
            criteria = model.criteria()
            literal_images = all(
                {values[v] for v in worlds
                 if model.same_outside(w, v, model.supports[p]) and values[v][p] == bit}
                == {overwrite(values[w], ((p, bit),))}
                for p in range(2) for bit in (0, 1) for w in worlds)
            assert criteria == literal_images
            atomic_cases += 1
            if criteria:
                e, f = check_model(model)
                endpoints += e
                nested += f
                valid_models += 1

    # Coarse predicates and genuinely non-Boolean coordinate domains, plus
    # a hidden coordinate shared by all stipulated supports.
    worlds = tuple(product(range(4), range(4), range(3), range(2)))
    values = {w: (w[0] & 1, w[1] & 1, int(w[2] == 0)) for w in worlds}
    hidden = Raw(worlds, tuple(frozenset((i, 3)) for i in range(3)), values)
    e, f = check_model(hidden)
    endpoints += e
    nested += f

    # The exact full-product failure from the note.
    feasible = tuple(w for w in product((0, 1), repeat=5) if w[3] == w[4])
    values = {w: (w[0], w[1], w[2] ^ w[3]) for w in feasible}
    bad = Raw(feasible, (frozenset((0, 3)), frozenset((1, 4)),
                         frozenset((2, 3, 4))), values)
    assert bad.criteria()
    w, v = (0, 0, 0, 0, 0), (1, 1, 0, 1, 1)
    assert v in bad.successors(('and', 0, 1), w)
    assert values[v] not in cube_successors(('and', 0, 1), values[w])
    bad.clear()

    # Empty visible vocabulary on a nonempty product maps onto the empty tuple.
    empty = Raw(((0,), (1,)), (), {(0,): (), (1,): ()})
    assert empty.criteria() and set(empty.values.values()) == {()}
    print(f'PASS: {atomic_cases} exhaustive local two-atom inputs on Boolean products of dimensions 1-3.')
    print(f'PASS: {valid_models} admissible small models and one 96-world hidden-value model.')
    print(f'PASS: {endpoints} exact endpoint-image checks and {nested} nested formula/world checks.')
    print('PASS: non-product counterexample and empty-vocabulary boundary.')


if __name__ == '__main__':
    main()
