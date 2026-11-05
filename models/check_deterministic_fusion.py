"""Direct finite checks of deterministic fusion and the affine forest bound.

Standard library only. Coordinate endpoints, subspace enumeration, and
decision tables are independent of the formulas in the mathematical note.
"""
from itertools import combinations, product
import random


def dim(space):
    assert len(space) and len(space) & (len(space) - 1) == 0
    return len(space).bit_length() - 1


def mobius(values, n):
    result = list(values)
    for i in range(n):
        for j in range(1 << n):
            if j >> i & 1:
                result[j] -= result[j ^ (1 << i)]
    return result


def endpoints(worlds, supports, values, assignment):
    """Group actual raw rows, without using an equality/affine normal form."""
    assigned = tuple(i for i, b in enumerate(assignment) if b != -1)
    writable = frozenset().union(*(supports[i] for i in assigned))
    fixed = tuple(i for i in range(len(worlds[0])) if i not in writable)
    groups = {}
    for v in worlds:
        key = tuple(v[i] for i in fixed), tuple(values[v][i] for i in assigned)
        groups.setdefault(key, set()).add(v)
    target = tuple(assignment[i] for i in assigned)
    return {w: groups.get((tuple(w[i] for i in fixed), target), set())
            for w in worlds}


def equality_model(n, hidden_owners, tables, duplicate_private=False):
    # A class owner -1 supplies a guard outside all writable supports.
    owner_lists = [(i, i) if duplicate_private else (i,) for i in range(n)]
    owner_lists += list(hidden_owners)
    coordinates = [(c, owner) for c, owners in enumerate(owner_lists)
                   for owner in owners]
    supports = tuple(frozenset(j for j, (_, owner) in enumerate(coordinates)
                               if owner == i) for i in range(n))
    incident = [tuple(t for t, owners in enumerate(hidden_owners) if i in owners)
                for i in range(n)]
    classes = list(product((0, 1), repeat=len(owner_lists)))
    worlds = [tuple(bits[c] for c, _ in coordinates) for bits in classes]
    values, hidden = {}, {}
    for w, bits in zip(worlds, classes):
        h = bits[n:]
        hidden[w] = h
        values[w] = tuple(bits[i] ^ (tables[i] >> sum(h[t] << k for k, t
                          in enumerate(incident[i])) & 1) for i in range(n))
    return worlds, supports, values, hidden


def check_equalities():
    rng = random.Random(20261105)
    shapes = [(2, ((0, 1),)), (2, ((0, 1), (0, 1))),
              (2, ((0, 1, -1),)), (2, ((0, -1), (1, -1))),
              (2, ((0, 0, 1), (0, 1, -1))),
              (3, ((0, 1), (1, 2), (0, 1, 2)))]
    models = checked = 0
    for n, owners in shapes:
        incident = [sum(i in c for c in owners) for i in range(n)]
        choices = [range(1 << (1 << k)) for k in incident]
        masks = list(product(*choices)) if n == 2 else [
            tuple(rng.randrange(len(c)) for c in choices) for _ in range(12)]
        expected_m = [0] * (1 << n)
        for c in owners:
            if -1 not in c:
                expected_m[sum(1 << i for i in set(c))] += 1
        for tables in masks:
            worlds, supports, values, hidden = equality_model(
                n, owners, tables, duplicate_private=models % 2 == 0)
            canonical = {w: values[w] + hidden[w] for w in worlds}
            assert len(set(canonical.values())) == len(worlds)
            r = [None] * (1 << n)
            for assignment in product((-1, 0, 1), repeat=n):
                j = sum(1 << i for i, b in enumerate(assignment) if b != -1)
                released = {t for t, c in enumerate(owners)
                            if -1 not in c and all(j >> i & 1 for i in c)}
                actual = endpoints(worlds, supports, values, assignment)
                for w in worlds:
                    target = tuple(values[w][i] if b == -1 else b
                                   for i, b in enumerate(assignment))
                    expected = {v for v in worlds if values[v] == target and
                                all(hidden[v][t] == hidden[w][t]
                                    for t in range(len(owners)) if t not in released)}
                    assert actual[w] == expected
                    count = dim(actual[w])
                    assert r[j] is None or r[j] == count
                    r[j] = count
                    checked += 1
            assert mobius(r, n) == expected_m
            assert dim(worlds) - n - r[-1] == sum(-1 in c for c in owners)
            models += 1
    # Availability and minimality alone do not imply determinism.
    worlds = list(product((0, 1), repeat=2))
    values = {w: (w[0] & w[1],) for w in worlds}
    assert {len(v) for v in endpoints(worlds, ({0, 1},), values, (0,)).values()} == {3}
    assert {len(v) for v in endpoints(worlds, ({0, 1},), values, (1,)).values()} == {1}
    print(f'PASS: {models} equality models, arbitrary masks/guards/redundancy, '
          f'{checked} direct source/assignment comparisons and profile inversions.')


def parity_model(n, k):
    worlds = [a + x for a in product((0, 1), repeat=n)
              for x in product((0, 1), repeat=n) if sum(x) % 2 == 0]
    supports = tuple(frozenset((i, n + i)) for i in range(n))
    values = {w: tuple(w[i] ^ w[n + i] for i in range(n)) for w in worlds}
    decision = {w: sum(w[n:n + k]) % 2 for w in worlds}
    return worlds, supports, values, decision


def check_parity():
    cases = 0
    for n in range(2, 6):
        for k in range(1, n):
            worlds, supports, values, decision = parity_model(n, k)
            assert len(worlds) == 1 << (2 * n - 1)
            # Direct support minimality, not an assumption on the XOR formula.
            for i, support in enumerate(supports):
                for removed in support:
                    smaller = support - {removed}
                    assert any(all(w[j] == v[j] for j in smaller) and
                               values[w][i] != values[v][i]
                               for w in worlds for v in worlds)
            for assignment in product((-1, 0, 1), repeat=n):
                assigned = {i for i, b in enumerate(assignment) if b != -1}
                changes = bool(assigned & set(range(k))) and bool(
                    assigned & set(range(k, n)))
                actual = endpoints(worlds, supports, values, assignment)
                for w in worlds:
                    assert len(actual[w]) == 1 << max(0, len(assigned) - 1)
                    target = tuple(values[w][i] if b == -1 else b
                                   for i, b in enumerate(assignment))
                    assert {values[v] for v in actual[w]} == {target}
                    assert {decision[v] for v in actual[w]} == (
                        {0, 1} if changes else {decision[w]})
                    if len(assigned) == 1:
                        assert all(v[n:] == w[n:] for v in actual[w])
                    cases += 1
    r = [max(0, j.bit_count() - 1) for j in range(8)]
    assert mobius(r, 3)[7] == -1
    assert all(r[a] + r[b] <= r[a | b] + r[a & b]
               for a in range(8) for b in range(8))
    print(f'PASS: {cases} affine parity source/assignment cases, all splits for '
          'n=2,...,5, minimal supports, exact effects and negative Mobius boundary.')


def span(basis):
    result = {0}
    for v in basis:
        result |= {w ^ v for w in result}
    return result


def subspaces(m):
    """Every binary subspace once, through its unique reduced row echelon basis."""
    for rank in range(m + 1):
        for pivots in combinations(range(m), rank):
            free = [(i, j) for i, p in enumerate(pivots)
                    for j in range(p + 1, m) if j not in pivots]
            for bits in range(1 << len(free)):
                basis = [1 << p for p in pivots]
                for t, (i, j) in enumerate(free):
                    if bits >> t & 1:
                        basis[i] |= 1 << j
                yield span(basis)


def forest(n, edges):
    parent = list(range(n))
    def root(i):
        while parent[i] != i:
            i = parent[i]
        return i
    result = []
    for i, j in edges:
        a, b = root(i), root(j)
        if a != b:
            parent[a] = b
            result.append((i, j))
    return result


def check_affine_bound():
    spaces = tables = tight = uniform_tight = 0
    for n in (2, 3):
        for sizes in product((1, 2), repeat=n):
            masks, start = [], 0
            for size in sizes:
                masks.append(((1 << size) - 1) << start)
                start += size
            seen = set()
            for vectors in subspaces(start):
                key = tuple(sorted(vectors))
                assert key not in seen
                seen.add(key)
                private = [{v for v in vectors if v & ~s == 0} for s in masks]
                if any(len(p) == 1 for p in private):
                    continue  # Literal availability is impossible.
                spaces += 1
                pspace = span(set().union(*private))
                q = [dim(p) for p in private]
                assert dim(pspace) == sum(q)
                representatives, coset = [], {}
                for v in sorted(vectors):
                    if v not in coset:
                        index = len(representatives)
                        representatives.append(v)
                        coset.update({v ^ p: index for p in pspace})
                moves = {(i, j): [v for v in vectors if v & ~(masks[i] | masks[j]) == 0]
                         for i, j in combinations(range(n), 2)}
                for table in range(1 << len(representatives)):
                    decision = lambda v: table >> coset[v] & 1
                    witness, uniform = {}, {}
                    for edge, differences in moves.items():
                        changing = {w for w in representatives
                                    if any(decision(w) != decision(w ^ v) for v in differences)}
                        if changing:
                            w = next(iter(changing))
                            witness[edge] = next(v for v in differences
                                                 if decision(w) != decision(w ^ v))
                            uniform[edge] = len(changing) == len(representatives)
                    tree = forest(n, witness)
                    assert dim(vectors) >= sum(q) + len(tree)
                    assert dim(span(list(pspace) + [witness[e] for e in tree])) == dim(pspace) + len(tree)
                    for edge, v in witness.items():
                        for i in edge:
                            assert v & masks[i] not in private[i]
                            assert sizes[i] >= q[i] + 1
                    if len(tree) == n - 1 and start == 2 * n:
                        tight += 1
                        assert dim(vectors) == 2 * n - 1
                        nonedge = lambda i, j: i == j or tuple(sorted((i, j))) not in witness
                        assert all(not (nonedge(i, j) and nonedge(j, k)) or nonedge(i, k)
                                   for i, j, k in product(range(n), repeat=3))
                        # Quotient each 2-bit block by its private direction.
                        orthogonal = [next(c for c in range(1, 1 << start)
                                           if c & ~s == 0 and all((c & p).bit_count() % 2 == 0 for p in private[i]))
                                      for i, s in enumerate(masks)]
                        hidden = {tuple((w & c).bit_count() % 2 for c in orthogonal) for w in vectors}
                        assert hidden == {x for x in product((0, 1), repeat=n) if sum(x) % 2 == 0}
                        if all(uniform[e] for e in tree):
                            uniform_tight += 1
                            assert any(set(witness) == {(i, j) for i, j in combinations(range(n), 2)
                                                        if bool(cut >> i & 1) != bool(cut >> j & 1)}
                                       for cut in range(1, (1 << n) - 1))
                    tables += 1
    print(f'PASS: {spaces} exhaustive small linear spaces with private availability, '
          f'{tables} invariant decision tables; {tight} raw-optimal connected cases, '
          f'{uniform_tight} uniform complete-bipartite rigidity cases.')


def check_decision_rigidity():
    checked = 0
    for n in (2, 3, 4):
        hidden = [x for x in range(1 << n) if x.bit_count() % 2 == 0]
        index = {x: i for i, x in enumerate(hidden)}
        for table in range(1 << len(hidden)):
            d = lambda x: table >> index[x] & 1
            edges = {(i, j) for i, j in combinations(range(n), 2)
                     if any(d(x) != d(x ^ (1 << i) ^ (1 << j)) for x in hidden)}
            nonedge = lambda i, j: i == j or tuple(sorted((i, j))) not in edges
            assert all(not (nonedge(i, j) and nonedge(j, k)) or nonedge(i, k)
                       for i, j, k in product(range(n), repeat=3))
            if edges and all(all(d(x) != d(x ^ (1 << i) ^ (1 << j)) for x in hidden)
                             for i, j in edges):
                assert any(edges == {(i, j) for i, j in combinations(range(n), 2)
                                     if bool(cut >> i & 1) != bool(cut >> j & 1)}
                           for cut in range(1, (1 << n) - 1))
            checked += 1
    print(f'PASS: all {checked} Boolean decision functions on even-parity spaces '
          'for n=2,3,4; complete-multipartite and uniform bipartite rigidity.')


if __name__ == '__main__':
    check_equalities()
    check_parity()
    check_affine_bound()
    check_decision_rigidity()
