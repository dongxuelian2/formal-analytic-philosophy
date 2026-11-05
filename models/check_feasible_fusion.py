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


def construct(n, family, guarded=False, flat=False):
    """Build explicit coordinate tuples, then evaluate predicates locally."""
    if flat:
        worlds, values, decisions, keys = [], {}, {}, {}
        for bits in product((0, 1), repeat=n + len(family)):
            a, hidden = bits[:n], bits[n:]
            visible = tuple(a[i] ^ (sum(hidden[j] for j, c in enumerate(family)
                                       if i in c) % 2) for i in range(n))
            w = visible + hidden
            worlds.append(w)
            values[w], decisions[w], keys[bits] = visible, sum(hidden) % 2, w
        supports = tuple(frozenset((i,)) for i in range(n))
        return Raw(worlds, supports, values), decisions, keys, frozenset(range(n, n + len(family)))
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
        guard_indices = range(len(family)) if guarded is True else (guarded or ())
        w += tuple(hidden[j] for j in guard_indices)
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
    guard, gd, gkeys, gds = construct(n, family, flat=True)
    frozen, fd, fkeys, fds = construct(n, family, guarded=True)
    check_minimal(frozen, fd, fds)
    translate = {w: gkeys[k] for k, w in keys.items()}
    to_frozen = {w: fkeys[k] for k, w in keys.items()}
    check_minimal(raw, decision, ds)
    check_minimal(guard, gd, gds)
    assert maximal_criterion(raw) and maximal_criterion(guard)
    assert set(raw.values.values()) == set(product((0, 1), repeat=n))
    for w in raw.worlds:
        assert raw.values[w] == guard.values[translate[w]]
        assert decision[w] == gd[translate[w]] == fd[to_frozen[w]]
        for p in range(n):
            for literal in (p, ('not', p)):
                actual = raw.successors(literal, w)
                assert len(actual) == 1
                assert {translate[v] for v in actual} == \
                    guard.successors(literal, translate[w])
                assert {to_frozen[v] for v in actual} == frozen.successors(literal, to_frozen[w])

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
            assert {to_frozen[v] for v in raw.worlds if translate[v] in guarded} == \
                frozen.successors(a, to_frozen[w])
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
    guard, gd, gkeys, _ = construct(n, family, flat=True)
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






def equality_size_checks():
    def minimal(xs):
        return {x for x in xs if not any(y != x and y & x == y for y in xs)}

    checked = bounded = rigid = 0
    for n, maxr in ((1,3),(2,3),(3,2)):
      for r in range(1,maxr+1):
        for owners in product(range(1<<n),repeat=r): # zero means uncovered/guarded
          for table in range(1<<(1<<r)):
            val = lambda w: table>>w&1
            essential = {k for k in range(r) if any(val(w)!=val(w^(1<<k)) for w in range(1<<r))}
            predicted = minimal({owners[k] for k in essential if owners[k]})
            actual = set()
            pointwise = {}
            for J in range(1<<n):
              released = sum(1<<k for k,C in enumerate(owners) if C and C&J==C)
              changing_sources = {w for w in range(1<<r) if any((w^v)&~released==0 and val(w)!=val(v) for v in range(1<<r))}
              if changing_sources: actual.add(J)
              pointwise[J] = changing_sources
            actual = minimal(actual)
            assert actual == predicted
            checked += 1
            private = all((1<<i) in owners for i in range(n))
            if private and actual and all(C.bit_count()>=2 for C in actual):
              assert r >= n+len(actual)
              assert sum(max(1,C.bit_count()) for C in owners) >= n+sum(C.bit_count() for C in actual)
              for i in range(n):
                assert sum(bool(C & (1 << i)) for C in owners) >= 1 + sum(bool(C & (1 << i)) for C in actual)
              bounded += 1
              uniform = all(len(pointwise[J]) in (0,1<<r) for J in range(1<<n))
              if uniform and r == n+len(actual):
                hidden = sum(1<<k for k,C in enumerate(owners) if C in actual)
                assert all(val(w) == (val(0)^((w&hidden).bit_count()%2)) for w in range(1<<r))
                rigid += 1
    print(f'PASS: {checked} owner-list/decision-table instances; {bounded} nonempty nonsingleton coalition models satisfying private-class availability; {rigid} minimum-world uniform instances with forced parity.')


def partial_guard_and_recovery():
    # Pair and triple effects; compare independently enumerated raw endpoints.
    n, family = 4, (frozenset((0, 1)), frozenset((1, 2, 3)))
    raw, d, keys, _ = construct(n, family)
    partial, pd, pkeys, _ = construct(n, family, guarded=(1,))
    translate = {w: pkeys[k] for k, w in keys.items()}
    inverse = {v: w for w, v in translate.items()}
    for assignment in product((-1, 0, 1), repeat=n):
        j = frozenset(i for i, b in enumerate(assignment) if b != -1)
        if not j:
            continue
        a = clause(assignment)
        for w in raw.worlds:
            actual = raw.successors(a, w)
            other = {inverse[v] for v in partial.successors(a, translate[w])}
            assert (actual == other) == (not family[1] <= j)
            support = frozenset().union(*(raw.supports[i] for i in j))
            fibre = {v for v in raw.worlds if raw.same_outside(w, v, support)}
            assert {d[v] for v in actual} == {d[v] for v in fibre}
            assert d[w] in {d[v] for v in actual}
    # Compute reset components by BFS, not the release-count formula.
    for k in (1, 2, 3):
        for jmask in range(1, 1 << n):
            j = frozenset(i for i in range(n) if jmask >> i & 1)
            small = [frozenset(c) for r in range(1, min(k, len(j)) + 1)
                     for c in combinations(j, r)]
            supports = [frozenset().union(*(raw.supports[i] for i in c)) for c in small]
            total = frozenset().union(*(raw.supports[i] for i in j))
            for w in raw.worlds[:4]:
                reached, todo = {w}, [w]
                while todo:
                    u = todo.pop()
                    for v in raw.worlds:
                        if v not in reached and any(raw.same_outside(u, v, s) for s in supports):
                            reached.add(v)
                            todo.append(v)
                fibre = {v for v in raw.worlds if raw.same_outside(w, v, total)}
                assert (reached == fibre) == all(len(c) <= k for c in family if c <= j)
    raw.clear()
    partial.clear()
    print('PASS: mixed pair/triple partial guards, decision spectra, and exact reset-recovery widths.')


def quotient_intersection_boundary():
    worlds = tuple((r, c) for r in range(4) for c in range(4)
                   if c == r or c == (r + 1) % 4)
    model = Raw(worlds, (frozenset((1,)), frozenset((0,))),
                {w: (w[1] % 2, w[0] % 2) for w in worlds})
    assert maximal_criterion(model)
    forward = {v for u in model.successors(0, (0, 0)) for v in model.successors(1, u)}
    reverse = {v for u in model.successors(1, (0, 0)) for v in model.successors(0, u)}
    assert forward == {(1, 1)} and reverse == {(3, 3)}
    assert not forward & reverse
    assert cube_successors(1, (1, 0)) == cube_successors(0, (0, 1)) == {(1, 1)}
    model.clear()
    print('PASS: quotient preserves base conditionals but not program intersection.')


def check_boundary(overlap):
    n = 4
    if overlap:
        worlds = tuple(a + (h, h) for a in product((0, 1), repeat=4) for h in (0, 1))
        supports = tuple(frozenset((i, 4 if i < 2 else 5)) for i in range(4))
        hidden = lambda w: w[4:5]
        values = lambda w: tuple(w[i] ^ w[4] for i in range(4))
        decision = lambda w: w[4]
    else:
        worlds = tuple(a + x for a in product((0, 1), repeat=4)
                       for x in product((0, 1), repeat=4) if sum(x) % 2 == 0)
        supports = tuple(frozenset((i, 4+i)) for i in range(4))
        hidden = lambda w: w[4:7]
        values = lambda w: tuple(w[i] ^ w[4+i] for i in range(4))
        decision = lambda w: w[4] ^ w[5]
    def same_outside(w, v, support):
        return all(x == y for i, (x, y) in enumerate(zip(w, v)) if i not in support)
    keys = {w: values(w) + hidden(w) for w in worlds}
    assert len(set(keys.values())) == len(worlds)
    assert set(keys.values()) == set(product((0, 1), repeat=len(keys[worlds[0]])))
    for i, support in enumerate(supports):
        assert all(values(w)[i] == values(v)[i] for w in worlds for v in worlds
                   if all(w[k] == v[k] for k in support))
        for removed in support:
            smaller = support - {removed}
            assert any(values(w)[i] != values(v)[i] for w in worlds for v in worlds
                       if all(w[k] == v[k] for k in smaller))
    comparisons = 0
    for assignment in product((-1, 0, 1), repeat=4):
        J = {i for i, b in enumerate(assignment) if b != -1}
        support = frozenset().union(*(supports[i] for i in J))
        expected_change = bool(J & {0, 1}) and bool(J & {2, 3})
        for w in worlds:
            endpoints = {v for v in worlds if same_outside(w, v, support)
                         and all(values(v)[i] == assignment[i] for i in J)}
            assert endpoints
            assert any(decision(v) != decision(w) for v in endpoints) == expected_change
            if len(J) == 1:
                target = tuple(assignment[i] if i in J else values(w)[i] for i in range(4)) + hidden(w)
                assert {keys[v] for v in endpoints} == {target}
            comparisons += 1
    assert len(worlds) == (32 if overlap else 128)
    assert len(worlds[0]) == (6 if overlap else 8)
    assert all(len(s) == 2 for s in supports)
    print('PASS', 'overlap' if overlap else 'affine K2,2', comparisons, 'source/assignment comparisons')


if __name__ == '__main__':
    main()
    equality_size_checks()
    partial_guard_and_recovery()
    quotient_intersection_boundary()
    check_boundary(True)
    check_boundary(False)
