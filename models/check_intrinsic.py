"""Finite intrinsic representation checks; Python standard library only."""
from itertools import product, permutations, combinations
from check_variation import Model, neg, conj, disj


def partitions(n):
    def visit(a):
        if len(a) == n:
            yield tuple(a)
        else:
            for v in range(max(a, default=-1) + 2):
                yield from visit(a + [v])
    yield from visit([])


def relation(labels):
    n = len(labels)
    return sum(1 << (i*n+j) for i in range(n) for j in range(n) if labels[i] == labels[j])


def compose(e, f, n):
    return sum(1 << (i*n+j) for i in range(n) for j in range(n)
               if any(e >> (i*n+k) & 1 and f >> (k*n+j) & 1 for k in range(n)))


def join(e, f, n):
    r = e | f
    while True:
        s = r | compose(r, r, n)
        if s == r: return r
        r = s


def completion_test(b, n):
    delta, top = relation(tuple(range(n))), (1 << (n*n))-1
    if delta not in b or top not in b: return False
    joins = {(e, f): join(e, f, n) for e in b for f in b}
    for e, f in product(b, repeat=2):
        if e & f not in b or joins[e, f] not in b: return False
        if compose(e, f, n) != compose(f, e, n): return False
    for e in b:
        if not any((e & f) == delta and joins[e, f] == top for f in b): return False
    return all((e & joins[f, g]) == joins[e & f, e & g]
               for e, f, g in product(b, repeat=3))


def complement(e, b, n):
    delta, top = relation(tuple(range(n))), (1 << (n*n))-1
    candidates = [f for f in b if (e & f) == delta and join(e, f, n) == top]
    assert len(candidates) == 1
    return candidates[0]


def truth_kernel(p, n):
    return relation(tuple((p >> i) & 1 for i in range(n)))


def filter_target(e, p, n):
    return sum(1 << (i*n+j) for i in range(n) for j in range(n)
               if (e >> (i*n+j) & 1) and (p >> j & 1))


def signature(a, atom_data, n):
    if isinstance(a, str):
        e, p = atom_data[a]
        return {(e, p)}, {(e, ((1 << n)-1) ^ p)}
    if a[0] == 'not':
        t, f = signature(a[1], atom_data, n)
        return f, t
    t1, f1 = signature(a[1], atom_data, n)
    t2, f2 = signature(a[2], atom_data, n)
    def fusion(x, y):
        return {(join(e, f, n), p & q) for e, p in x for f, q in y}
    if a[0] == 'and': return fusion(t1, t2), f1 | f2 | fusion(f1, f2)
    return t1 | t2 | fusion(t1, t2), fusion(f1, f2)


def generated_relation(a, data, n):
    r = 0
    for e, p in signature(a, data, n)[0]: r |= filter_target(e, p, n)
    return r


def reconstruct(b, n):
    delta = relation(tuple(range(n)))
    atoms = [e for e in b if e != delta and not any(f != delta and f != e and (f & e) == f for f in b)]
    coords = []
    for e in atoms:
        k = complement(e, b, n)
        reps = [min(j for j in range(n) if k >> (i*n+j) & 1) for i in range(n)]
        names = {v: i for i, v in enumerate(sorted(set(reps)))}
        coords.append(tuple(names[v] for v in reps))
    tuples = tuple(tuple(c[w] for c in coords) for w in range(n))
    domains = tuple(tuple(sorted(set(c))) for c in coords)
    assert len(set(tuples)) == n and set(tuples) == set(product(*domains))
    return atoms, tuples, domains


def main():
    n = 4
    eq = sorted({relation(p) for p in partitions(n)})
    delta, top = relation(tuple(range(n))), (1 << (n*n))-1
    middle = [e for e in eq if e not in (delta, top)]
    # Exhaustive relation-space search, without supplying coordinate partitions.
    completions = []
    for mask in range(1 << len(middle)):
        b = {delta, top} | {e for i, e in enumerate(middle) if mask >> i & 1}
        # At most log2(4)=2 Boolean atoms, so at most 4 lattice elements.
        if len(b) <= 4 and completion_test(b, n): completions.append(b)
    assert len(eq) == 15 and len(completions) == 4

    # Independently enumerate direct products and all world bijections.
    direct = set()
    for domains in [((0, 1, 2, 3),), ((0, 1), (0, 1))]:
        for points in permutations(tuple(product(*domains))):
            possibilities = []
            for mask in range(1 << len(domains)):
                support = {i for i in range(len(domains)) if mask >> i & 1}
                e = relation(tuple(tuple(w[i] for i in range(len(domains)) if i not in support) for w in points))
                for p in range(1 << n):
                    if all(((p >> i) & 1) == ((p >> j) & 1)
                           for i, j in product(range(n), repeat=2)
                           if all(points[i][k] == points[j][k] for k in support)):
                        possibilities.append((e, p))
            direct.update(product(possibilities, repeat=2))

    abstract = set()
    formula_checks = 0
    lits = ['p', 'q', neg('p'), neg('q')]
    formulas = lits + [op(a, b) for op in (conj, disj) for a, b in product(lits, repeat=2)]
    for b in completions:
        possibilities = [(e, p) for e in b for p in range(1 << n)
                         if complement(e, b, n) & ~truth_kernel(p, n) == 0]
        abstract.update(product(possibilities, repeat=2))
        atoms, points, domains = reconstruct(b, n)
        for left, right in product(possibilities, repeat=2):
            data = dict(zip(('p', 'q'), (left, right)))
            coordinate_atoms = {}
            for name, (e, p) in data.items():
                support = {i for i, a in enumerate(atoms) if a & e == a}
                coordinate_atoms[name] = (support, {points[i] for i in range(n) if p >> i & 1})
                assert filter_target(e, p, n) | filter_target(e, ((1 << n)-1) ^ p, n) == e
            model = Model(domains, coordinate_atoms)
            for formula in formulas:
                actual = sum(1 << (i*n+j) for i in range(n) for j in range(n)
                             if points[j] in model.select(points[i], formula))
                assert actual == generated_relation(formula, data, n)
                formula_checks += 1
    assert abstract == direct
    # Every possible two-atom intrinsic input: 15^2 equivalence pairs x 16^2 colors.
    for e, f in product(eq, repeat=2):
        for p, q in product(range(16), repeat=2):
            candidate = ((e, p), (f, q))
            assert (candidate in abstract) == (candidate in direct)

    e = relation((0, 0, 1, 1))
    assert ((e, 0b0101), (e, 0b1001)) not in abstract
    assert all(sum(p >> i & 1 for i in block) == 1
               for p in (0b0101, 0b1001) for block in ((0, 1), (2, 3)))
    # Positive example: aligned joint colors, same geometry.
    assert ((e, 0b0101), (e, 0b0101)) in abstract
    # Equal positive conditional relations do not make negation well-defined.
    ex, ey = relation((0, 0, 1, 1)), relation((0, 1, 0, 1))
    data = {'p': (ex, 0b0101), 'q': (ey, 0b0011)}
    a, b = conj('p', neg('p')), conj('q', neg('q'))
    assert generated_relation(a, data, n) == generated_relation(b, data, n) == 0
    assert generated_relation(neg(a), data, n) == ex
    assert generated_relation(neg(b), data, n) == ey
    # Singleton / zero-coordinate representation.
    assert completion_test({1}, 1)
    assert reconstruct({1}, 1)[1] == ((),)
    print('4 worlds: all 15 equivalences and 4 Boolean commuting completions found.')
    print(f'All 57,600 two-atom equivalence/color inputs agree with independent direct-product enumeration; {len(abstract)} representable.')
    print(f'{formula_checks} intrinsic-vs-coordinate formula matrices agree, including disjunction fusion.')
    print('Joint-color obstruction, negation obstruction, aligned example, and singleton case passed.')


if __name__ == '__main__': main()
