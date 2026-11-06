"""Small independent checks for the colored-completion complexity reduction.
Standard library only. Enumeration supports, but does not prove, NP-hardness.
"""
from collections import Counter, defaultdict
from itertools import product, combinations_with_replacement, permutations
import random


def canonical_pairs(pairs):
    return tuple(sorted(pairs))


def direct_fork_alignment(cells):
    """Search actual cellwise coordinate bijections, fixing cell 00's labels.
    Independent of the integer-table/marginal solver. Intended for tiny K.
    """
    first = cells[0]
    for c01, c10, c11 in product(*(set(permutations(c)) for c in cells[1:])):
        aligned = (first, c01, c10, c11)
        if all(aligned[0][s][0] == aligned[1][s][0]
               and aligned[2][s][0] == aligned[3][s][0]
               and aligned[0][s][1] == aligned[2][s][1]
               and aligned[1][s][1] == aligned[3][s][1]
               for s in range(len(first))):
            return True
    return False


def fork_profiles(k):
    profiles = set()
    for rows in combinations_with_replacement(tuple(product(range(2), repeat=4)), k):
        profiles.add(tuple(canonical_pairs((r[x], r[2+y]) for r in rows)
                           for x, y in product(range(2), repeat=2)))
    return profiles


def partial_valid(p, n):
    for i in range(n):
        row = [p[i*n+j] for j in range(n) if p[i*n+j] >= 0]
        col = [p[j*n+i] for j in range(n) if p[j*n+i] >= 0]
        if len(row) != len(set(row)) or len(col) != len(set(col)):
            return False
    return True


def margins(p, n):
    u = {(a,b) for a,b in product(range(n), repeat=2) if p[a*n+b] < 0}
    v = {(a,c) for a,c in product(range(n), repeat=2)
         if c not in p[a*n:(a+1)*n]}
    t = {(b,c) for b,c in product(range(n), repeat=2)
         if all(p[a*n+b] != c for a in range(n))}
    return u,v,t


def table_solution(u, v, t):
    """Exact cover on the three pair margins, independent of Latin arrays."""
    if not u:
        return () if not v and not t else None
    a,b = min(u, key=lambda ab: sum((ab[1],c) in t for aa,c in v if aa==ab[0]))
    for aa,c in sorted(v):
        if aa == a and (b,c) in t:
            rest = table_solution(u-{(a,b)}, v-{(a,c)}, t-{(b,c)})
            if rest is not None:
                return ((a,b,c),)+rest
    return None


def reduction_cells(u,v,t):
    d = Counter(a for a,b in u)
    return (tuple((a,a) for a in sorted(d) for _ in range(d[a])),
            tuple(sorted(v)), tuple(sorted((b,a) for a,b in u)), tuple(sorted(t)))


def verify_product_witness(cells, triples, n):
    """Build the actual bijection and check all bit-locality/support equations."""
    k = len(triples)
    if not k:
        return
    world_to_tuple = {}
    truth = {}
    bits = max(1, (n-1).bit_length())
    for index, (x,y) in enumerate(product(range(2),repeat=2)):
        queues = defaultdict(list)
        for s,(a,b,c) in enumerate(triples):
            queues[((a,b)[x], (a,c)[y])].append(s)
        for old,(alpha,beta) in enumerate(cells[index]):
            s = queues[(alpha,beta)].pop()
            w = (old,x,y)
            world_to_tuple[w] = (s,x,y)
            truth[w] = tuple((alpha>>j)&1 for j in range(bits)) + tuple((beta>>j)&1 for j in range(bits))
        assert not any(queues.values())
    assert len(set(world_to_tuple.values())) == 4*k
    worlds = tuple(world_to_tuple)
    for w,z in product(worlds, repeat=2):
        a,b = world_to_tuple[w], world_to_tuple[z]
        assert (w[2]==z[2]) == (a[2]==b[2])  # E agreement outside S,X
        assert (w[1]==z[1]) == (a[1]==b[1])  # F agreement outside S,Y
        if a[:2] == b[:2]:
            assert truth[w][:bits] == truth[z][:bits]
        if (a[0],a[2]) == (b[0],b[2]):
            assert truth[w][bits:] == truth[z][bits:]


def main():
    fork_cases = 0
    for k in (1,2):
        options = tuple(combinations_with_replacement(tuple(product(range(2),repeat=2)), k))
        attainable = fork_profiles(k)
        for cells in product(options, repeat=4):
            assert direct_fork_alignment(cells) == (cells in attainable)
            fork_cases += 1
    parity = (((0,0),(1,1)),)*3 + (((0,1),(1,0)),)
    assert not direct_fork_alignment(parity)
    print(f'Fork criterion: {fork_cases} binary-color instances, all matched actual coordinate relabelings.')

    latin_cases = positives = witness_cases = 0
    rng = random.Random(604)
    for n in (1,2,3):
        complete = [p for p in product(range(n),repeat=n*n) if partial_valid(p,n)]
        assert len(complete) == {1:1,2:2,3:12}[n]
        for p in product(range(-1,n),repeat=n*n):
            if not partial_valid(p,n):
                continue
            expected = any(all(a<0 or a==b for a,b in zip(p,q)) for q in complete)
            u,v,t = margins(p,n)
            sol = table_solution(u,v,t)
            assert (sol is not None) == expected
            latin_cases += 1
            positives += expected
            if sol is not None and (n<=2 or rng.random()<0.025):
                verify_product_witness(reduction_cells(u,v,t),sol,n)
                witness_cases += 1
            if 0 < len(u) <= 2:
                assert direct_fork_alignment(reduction_cells(u,v,t)) == expected
    print(f'Latin reduction: all {latin_cases} valid partial squares of orders 1,2,3 checked; {positives} completable.')
    print(f'Explicit Boolean product certificates: {witness_cases} positive instances checked (including empty-table boundary).')


if __name__ == '__main__':
    main()
