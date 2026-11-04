"""Check tautological resets and finite cyclic-group covers.
These finite checks do not establish the cited undecidability theorem.
"""
from itertools import product
from functools import lru_cache
import random
from check_variation import Model, disj, neg


def subsets(n):
    return [frozenset(i for i in range(n) if mask>>i&1) for mask in range(1<<n)]


def evaluate(formulas, worlds, successors, valuation):
    universe = frozenset(worlds)
    @lru_cache(None)
    def truth(f):
        if isinstance(f,str):
            return frozenset(valuation[f])
        if f[0]=='not':
            return universe-truth(f[1])
        if f[0]=='and':
            return truth(f[1]) & truth(f[2])
        if f[0]=='box':
            target = truth(f[2])
            return frozenset(w for w in worlds if successors[f[1]][w] <= target)
        raise ValueError(f)
    return [truth(f) for f in formulas]


def check(domains, supports, base, rng):
    old_worlds = tuple(product(*(range(d) for d in domains)))
    union = frozenset().union(*supports)
    component = tuple(w for w in old_worlds if all(w[c]==base[c] for c in range(len(domains)) if c not in union))
    incidences = [tuple(sorted(s)) for s in supports]
    factors = [tuple(product(*(range(domains[c]) for c in coords))) for coords in incidences]
    source = tuple(product(*factors))
    def image(x):
        return tuple(sum(x[i][incidences[i].index(c)] for i in range(len(supports)) if c in supports[i]) % domains[c]
                     if c in union else base[c] for c in range(len(domains)))
    h = {x:image(x) for x in source}
    assert set(h.values()) == set(component)
    src_rel = [{x:frozenset(x[:i]+(value,)+x[i+1:] for value in factors[i]) for x in source}
               for i in range(len(supports))]
    old_rel = [{w:frozenset(v for v in component if all(w[c]==v[c] for c in range(len(domains)) if c not in s))
                for w in component} for s in supports]
    edges = 0
    for i in range(len(supports)):
        for x in source:
            assert {h[y] for y in src_rel[i][x]} == set(old_rel[i][h[x]])
            edges += len(src_rel[i][x])

    # Marker truths are arbitrary local tables, not necessarily constant.
    atoms = {}
    for i,s in enumerate(supports):
        choices = {tuple(w[c] for c in sorted(s)) for w in old_worlds}
        selected = {a for a in choices if rng.randrange(2)}
        atoms[f'q{i}'] = (s,{w for w in old_worlds if tuple(w[c] for c in sorted(s)) in selected})
    raw = Model([range(d) for d in domains],atoms)
    for i in range(len(supports)):
        for w in component:
            assert raw.select(w,disj(f'q{i}',neg(f'q{i}'))) == set(old_rel[i][w])

    valuation = {p:{w for w in component if rng.randrange(2)} for p in ('a','b')}
    pulled = {p:{x for x in source if h[x] in valuation[p]} for p in valuation}
    formulas = ['a','b']
    for _ in range(80):
        kind = rng.randrange(3)
        if kind==0:
            formulas.append(('not',rng.choice(formulas)))
        elif kind==1:
            formulas.append(('and',rng.choice(formulas),rng.choice(formulas)))
        else:
            formulas.append(('box',rng.randrange(len(supports)),rng.choice(formulas)))
    old_truth = evaluate(formulas,component,old_rel,valuation)
    src_truth = evaluate(formulas,source,src_rel,pulled)
    for a,b in zip(old_truth,src_truth):
        assert b == frozenset(x for x in source if h[x] in a)
    return edges,len(formulas)*len(source)


def main():
    rng = random.Random(1426)
    cases = edges = evaluations = 0
    # Exhaust all triples of supports on one/two coordinates, including
    # empty, equal and overlapping supports, and nonbinary/singleton domains.
    for domains in ((1,),(2,),(3,),(1,2),(2,2),(2,3),(3,2)):
        for ss in product(subsets(len(domains)),repeat=3):
            base = tuple(d-1 for d in domains)
            e,f = check(domains,ss,base,rng)
            cases += 1; edges += e; evaluations += f
    # All three-coordinate support patterns on the Boolean cube.
    for ss in product(subsets(3),repeat=3):
        e,f = check((2,2,2),ss,(1,1,1),rng)
        cases += 1; edges += e; evaluations += f
    print(f'{cases} support/domain patterns: every cover is onto its generated component and satisfies exact successor-image equality.')
    print(f'{edges} source edges and {evaluations} nested modal formula/world evaluations checked.')
    print('Tautological resets also checked using the independent exact-verifier evaluator with arbitrary local marker truths.')


if __name__=='__main__':
    main()
