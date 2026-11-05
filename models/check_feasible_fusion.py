"""Finite checks of feasible-domain fusion; standard library only.

The reference endpoint evaluator is the per-world bilateral verifier
recursion in check_boolean_quotient, not the coalition construction formula.
Assertions supplement the written proofs and do not establish novelty.
"""
from itertools import combinations, product
import random

from check_boolean_quotient import Raw, cube_successors, evaluate, local_atoms


def clause(assignment):
    literals = [i if b else ('not', i)
                for i, b in enumerate(assignment) if b != -1]
    assert literals
    result = literals[0]
    for literal in literals[1:]:
        result = ('and', result, literal)
    return result


def maximal_criterion(model):
    for p in range(model.n):
        others = frozenset().union(*(s for q, s in enumerate(model.supports)
                                    if q != p))
        for w in model.worlds:
            available = {model.values[v][p] for v in model.worlds
                         if model.same_outside(w, v, model.supports[p])}
            if available != {0, 1}:
                return False
            if any(model.values[v][p] != model.values[w][p]
                   for v in model.worlds if model.same_outside(w, v, others)):
                return False
    return True


def conjunction_quotient(model):
    for assignment in product((-1, 0, 1), repeat=model.n):
        if all(b == -1 for b in assignment):
            continue
        a = clause(assignment)
        for w in model.worlds:
            if {model.values[v] for v in model.successors(a, w)} != \
                    cube_successors(a, model.values[w]):
                return False
    return True


def small_criteria():
    count = accepted = 0
    for dimension in (1, 2):
        ambient = tuple(product((0, 1), repeat=dimension))
        for mask in range(1, 1 << len(ambient)):
            worlds = tuple(w for i, w in enumerate(ambient) if mask >> i & 1)
            options = local_atoms(worlds, dimension)
            for (sp, vp), (sq, vq) in product(options, repeat=2):
                model = Raw(worlds, (sp, sq), dict(zip(worlds, zip(vp, vq))))
                criterion = maximal_criterion(model)
                assert criterion == conjunction_quotient(model)
                if criterion:
                    assert set(model.values.values()) == set(product((0, 1), repeat=2))
                    accepted += 1
                count += 1
                model.clear()

    # The earlier 16-world example passes atomic tests but fails the new
    # maximal-support test, with p AND q changing the unassigned feature r.
    worlds = tuple(w for w in product((0, 1), repeat=5) if w[3] == w[4])
    values = {w: (w[0], w[1], w[2] ^ w[3]) for w in worlds}
    bad = Raw(worlds, (frozenset((0, 3)), frozenset((1, 4)),
                       frozenset((2, 3, 4))), values)
    assert bad.criteria()
    assert not maximal_criterion(bad)
    assert not conjunction_quotient(bad)
    bad.clear()

    empty = Raw(((0,),), (), {(0,): ()})
    assert maximal_criterion(empty) and conjunction_quotient(empty)
    one = Raw(((0,), (1,)), (frozenset((0,)),), {(0,): (0,), (1,): (1,)})
    assert maximal_criterion(one) and conjunction_quotient(one)
    one.clear()
    print(f'PASS: {count} exhaustive feasible local two-atom inputs, {accepted} accepted.')
    print('PASS: maximal test rejects the old non-product counterexample; empty/singleton boundaries.')


def antichains(n):
    candidates = [frozenset(c) for k in range(2, n + 1)
                  for c in combinations(range(n), k)]
    for mask in range(1, 1 << len(candidates)):
        family = tuple(c for i, c in enumerate(candidates) if mask >> i & 1)
        if all(not a < b and not b < a for a, b in combinations(family, 2)):
            yield family


def construct(n, family, guarded=False):
    """Build explicit coordinate tuples, then evaluate predicates locally."""
    columns = [(j, i) for j, c in enumerate(family) for i in sorted(c)]
    positions = {pair: n + k for k, pair in enumerate(columns)}
    supports = tuple(frozenset([i] + [positions[j, i]
                                      for j, c in enumerate(family) if i in c])
                     for i in range(n))
    representatives = frozenset(positions[j, min(c)] for j, c in enumerate(family))
    worlds, values, decisions, keys = [], {}, {}, {}
    for bits in product((0, 1), repeat=n + len(family)):
        a, hidden = bits[:n], bits[n:]
        w = a + tuple(hidden[j] for j, i in columns)
        if guarded:
            w += hidden
        worlds.append(w)
        values[w] = tuple(sum(w[k] for k in s) % 2 for s in supports)
        decisions[w] = sum(w[k] for k in representatives) % 2
        keys[bits] = w
    model = Raw(worlds, supports, values)
    return model, decisions, keys, representatives


def check_minimal(model, decisions, decision_support):
    supports = model.supports + (decision_support,)
    labels = {w: model.values[w] + (decisions[w],) for w in model.worlds}
    for i, support in enumerate(supports):
        table = {}
        for w in model.worlds:
            key = tuple(w[k] for k in sorted(support))
            assert key not in table or table[key] == labels[w][i]
            table[key] = labels[w][i]
        for removed in support:
            groups = {}
            for w in model.worlds:
                key = tuple(w[k] for k in sorted(support - {removed}))
                groups.setdefault(key, set()).add(labels[w][i])
            assert any(len(bits) == 2 for bits in groups.values())
    assert all(not s & t for s, t in combinations(model.supports, 2))


def check_family(n, family, all_sources=True):
    raw, decision, keys, ds = construct(n, family)
    guard, gd, gkeys, gds = construct(n, family, guarded=True)
    translate = {w: gkeys[k] for k, w in keys.items()}
    check_minimal(raw, decision, ds)
    check_minimal(guard, gd, gds)
    assert maximal_criterion(raw) and maximal_criterion(guard)
    assert set(raw.values.values()) == set(product((0, 1), repeat=n))
    for w in raw.worlds:
        assert raw.values[w] == guard.values[translate[w]]
        assert decision[w] == gd[translate[w]]
        for p in range(n):
            for literal in (p, ('not', p)):
                actual = raw.successors(literal, w)
                assert len(actual) == 1
                assert {translate[v] for v in actual} == \
                    guard.successors(literal, translate[w])

    sources = raw.worlds if all_sources else raw.worlds[::max(1, len(raw.worlds) // 8)]
    count = 0
    for assignment in product((-1, 0, 1), repeat=n):
        j = frozenset(i for i, b in enumerate(assignment) if b != -1)
        if not j:
            continue
        a = clause(assignment)
        released = sum(c <= j for c in family)
        for w in sources:
            actual = raw.successors(a, w)
            guarded = guard.successors(a, translate[w])
            assert len(actual) == 2 ** released
            assert len(guarded) == 1
            assert {raw.values[v] for v in actual} == cube_successors(a, raw.values[w])
            assert {guard.values[v] for v in guarded} == cube_successors(a, raw.values[w])
            assert any(decision[v] != decision[w] for v in actual) == (released > 0)
            assert all(gd[v] == decision[w] for v in guarded)
            if not released:
                assert {translate[v] for v in actual} == guarded
            count += 1
    raw.clear()
    guard.clear()
    return count


def nested_width(n):
    family = (frozenset(range(n)),)
    raw, d, keys, _ = construct(n, family)
    guard, gd, gkeys, _ = construct(n, family, guarded=True)
    translate = {w: gkeys[k] for k, w in keys.items()}
    values = {w: raw.values[w] + (d[w],) for w in raw.worlds}
    gvalues = {w: guard.values[w] + (gd[w],) for w in guard.worlds}
    rng = random.Random(603 + n)

    def antecedent():
        omitted = rng.randrange(n)
        names = [p for p in range(n) if p != omitted]
        result = rng.choice(names)
        for _ in range(3):
            literal = rng.choice(names)
            if rng.randrange(2):
                literal = ('not', literal)
            result = (rng.choice(('and', 'or')), result, literal)
        return result

    pool = list(range(n + 1))
    for _ in range(60):
        op = rng.choice(('not', 'and', 'box'))
        if op == 'not':
            pool.append((op, rng.choice(pool)))
        elif op == 'and':
            pool.append((op, rng.choice(pool), rng.choice(pool)))
        else:
            pool.append((op, antecedent(), rng.choice(pool)))
    count = 0
    for phi in pool:
        for w in raw.worlds:
            assert evaluate(phi, w, values.__getitem__, raw.successors) == \
                evaluate(phi, translate[w], gvalues.__getitem__, guard.successors)
            count += 1
    joint = clause((1,) * n)
    witness = ('box', joint, ('not', n))
    for w in raw.worlds:
        if d[w] == 0:
            assert not evaluate(witness, w, values.__getitem__, raw.successors)
            assert evaluate(witness, translate[w], gvalues.__getitem__, guard.successors)

    # A genuinely feature-only nonconstant output is recomputed after an
    # assignment, rather than incorrectly treated as a framed writable bit.
    classifier = lambda bits: sum(bits) % 2
    fv = lambda w: raw.values[w] + (classifier(raw.values[w]),)
    qv = lambda bits: bits + (classifier(bits),)
    for phi in pool + [('box', joint, n)]:
        for w in raw.worlds:
            assert evaluate(phi, w, fv, raw.successors) == \
                evaluate(phi, raw.values[w], qv, cube_successors)
            count += 1
    raw.clear()
    guard.clear()
    return count


def sharp_feature_width(n):
    # m=n+1 writable features, and the first failure is width m-1=n.
    worlds = tuple(a + (c,) + (h,) * n
                   for a in product((0, 1), repeat=n)
                   for c, h in product((0, 1), repeat=2))
    supports = tuple(frozenset((i, n + 1 + i)) for i in range(n))
    supports += (frozenset((n, n + 1)),)
    values = {w: tuple(w[i] ^ w[n + 1] for i in range(n + 1)) for w in worlds}
    model = Raw(worlds, supports, values)
    assert model.criteria()  # Every literal has the exact Boolean image.
    assert not maximal_criterion(model)
    count = 0
    for assignment in product((-1, 0, 1), repeat=n + 1):
        width = sum(b != -1 for b in assignment)
        if not 0 < width < n:
            continue
        a = clause(assignment)
        for w in worlds:
            actual = model.successors(a, w)
            assert len(actual) == 1
            assert {values[v] for v in actual} == cube_successors(a, values[w])
            count += 1
    joint = clause((1,) * n + (-1,))
    for w in worlds:
        actual = model.successors(joint, w)
        assert {values[v][-1] for v in actual} == {0, 1}
        assert {values[v] for v in actual} != cube_successors(joint, values[w])
    model.clear()
    return count


def main():
    small_criteria()
    family_count = endpoint_count = 0
    for n in (2, 3):
        for family in antichains(n):
            endpoint_count += check_family(n, family)
            family_count += 1
    extra = [tuple(frozenset(c) for c in ((0, 1), (1, 2), (2, 3))),
             tuple(frozenset(c) for c in ((0, 1, 2), (1, 2, 3)))]
    for family in extra:
        endpoint_count += check_family(4, family, all_sources=False)
        family_count += 1
    nested_count = 0
    for n in (2, 3, 4, 5):
        endpoint_count += check_family(n, (frozenset(range(n)),))
        nested_count += nested_width(n)
        family_count += 1
    print(f'PASS: {family_count} coalition constructions/twins, including every antichain for n=2,3.')
    print(f'PASS: {endpoint_count} source/partial-assignment cases, exact counts, labels and decision effects.')
    print(f'PASS: {nested_count} nested width/classifier comparisons; separating widths 2 through 5.')
    print('PASS: disjoint minimal feature supports, literal availability, identical atomic reducts.')
    sharp_count = sum(sharp_feature_width(n) for n in (2, 3, 4))
    print(f'PASS: {sharp_count} lower-width feature-quotient cases; optimal m-1 failures for m=3,4,5.')


if __name__ == '__main__':
    main()
