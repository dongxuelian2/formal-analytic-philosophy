"""Independent Boolean-coordinate reduction audit; Python standard library only."""
from itertools import product
from functools import lru_cache
import random

N=3
W=tuple(product((0,1), repeat=N))

def neg(a): return ('not', a)
def And(a,b): return ('and', a,b)
def Or(a,b): return ('or', a,b)
def Box(a,b): return ('box', a,b)

# Semantic reference: per-world support families, no assignment normal form.
@lru_cache(None)
def makers(a,w):
    if isinstance(a,int):
        return (frozenset((1<<a,)),frozenset()) if w[a] else (frozenset(),frozenset((1<<a,)))
    if a[0]=='not':
        t,f=makers(a[1],w); return f,t
    t,f=makers(a[1],w); u,g=makers(a[2],w)
    pos=frozenset(s|r for s in t for r in u)
    negs=frozenset(s|r for s in f for r in g)
    return (pos,f|g|negs) if a[0]=='and' else (t|u|pos,negs)

@lru_cache(None)
def select(a,w):
    return frozenset(v for v in W for s in makers(a,v)[0]
        if all(s&(1<<i) or v[i]==w[i] for i in range(N)))

def evaluate(phi,w):
    if isinstance(phi,bool): return phi
    if isinstance(phi,int): return bool(w[phi])
    op=phi[0]
    if op=='not': return not evaluate(phi[1],w)
    if op=='and': return evaluate(phi[1],w) and evaluate(phi[2],w)
    if op=='or': return evaluate(phi[1],w) or evaluate(phi[2],w)
    return all(evaluate(phi[2],v) for v in select(phi[1],w))

# Operational calculus implementation: NNF, contextual three-way split,
# then consistent literal assignment. Duplicate branches intentionally retained.
def nnf(a,sign=True):
    if isinstance(a,int): return a if sign else neg(a)
    if a[0]=='not': return nnf(a[1],not sign)
    op=a[0] if sign else ('or' if a[0]=='and' else 'and')
    return (op,nnf(a[1],sign),nnf(a[2],sign))

def flatten_and(a):
    if isinstance(a,tuple) and a[0]=='and':
        return flatten_and(a[1])+flatten_and(a[2])
    return [a]

def clauses(items):
    items=sum((flatten_and(a) for a in items),[])
    for j,a in enumerate(items):
        if isinstance(a,tuple) and a[0]=='or':
            rest=items[:j]+items[j+1:]
            for extra in ([a[1]],[a[2]],[a[1],a[2]]):
                yield from clauses(rest+extra)
            return
    assignment={}
    for a in items:
        i,b=(a,1) if isinstance(a,int) else (a[1],0)
        if i in assignment and assignment[i]!=b: return
        assignment[i]=b
    yield assignment

def subst_prop(phi,t):
    if isinstance(phi,bool): return phi
    if isinstance(phi,int): return bool(t[phi]) if phi in t else phi
    if phi[0]=='not': return neg(subst_prop(phi[1],t))
    assert phi[0] in ('and','or')
    return (phi[0],subst_prop(phi[1],t),subst_prop(phi[2],t))

def normalize(phi):
    if isinstance(phi,(int,bool)): return phi
    if phi[0]=='not': return neg(normalize(phi[1]))
    if phi[0] in ('and','or'): return (phi[0],normalize(phi[1]),normalize(phi[2]))
    consequent=normalize(phi[2])
    result=True
    for t in clauses([nnf(phi[1])]): result=And(result,subst_prop(consequent,t))
    return result

rng=random.Random(39241)
def normal(depth):
    if depth<=0 or rng.random()<.25: return rng.randrange(N)
    op=rng.choice(('not','and','or'))
    return neg(normal(depth-1)) if op=='not' else (op,normal(depth-1),normal(depth-1))
def formula(depth):
    if depth<=0 or rng.random()<.2: return rng.randrange(N)
    op=rng.choice(('not','and','or','box'))
    if op=='not': return neg(formula(depth-1))
    return (op,normal(2) if op=='box' else formula(depth-1),formula(depth-1))

def main():
    literals=list(range(N))+[neg(i) for i in range(N)]
    pool=literals+[op(a,b) for op in (And,Or) for a,b in product(literals,repeat=2)]
    cases=0
    for _ in range(1500):
        d,a,b=(rng.choice(pool) for _ in range(3))
        left=And(d,Or(a,b))
        right=(And(d,a),And(d,b),And(And(d,a),b))
        for w in W:
            assert select(left,w)==frozenset().union(*(select(x,w) for x in right))
            cases+=1
    reduction_cases=0
    for _ in range(1500):
        phi=formula(4)
        reduced=normalize(phi)
        for w in W:
            assert evaluate(phi,w)==evaluate(reduced,w), (phi,w,reduced)
            reduction_cases+=1
    # Last-write-wins: every pair of partial assignments, all worlds.
    assignments=list(product((-1,0,1),repeat=N))
    overwrite_cases=0
    for t,u,w in product(assignments,assignments,W):
        wt=tuple(w[i] if t[i]==-1 else t[i] for i in range(N))
        wtu=tuple(wt[i] if u[i]==-1 else u[i] for i in range(N))
        merged=tuple(u[i] if u[i]!=-1 else t[i] for i in range(N))
        direct=tuple(w[i] if merged[i]==-1 else merged[i] for i in range(N))
        assert wtu==direct
        overwrite_cases+=1
    assert not any(evaluate(Box(0,Box(neg(0),0)),w) for w in W)
    print(f'PASS: {cases} contextual split checks, {reduction_cases} full nested reduction checks, {overwrite_cases} last-write-wins checks.')
    print('Checks support but do not replace the general soundness/completeness proof.')



def check_qbf():
    cases=0
    for prefix in product((False,True), repeat=N):
        for _ in range(50):
            matrix=normal(3)
            def solve(i,w):
                if i==N: return evaluate(matrix,w)
                values=[solve(i+1,w[:i]+(b,)+w[i+1:]) for b in (0,1)]
                return all(values) if prefix[i] else any(values)
            expected=solve(0,(0,)*N)
            translated=matrix
            for i in reversed(range(N)):
                reset=Or(i,neg(i))
                translated=Box(reset,translated) if prefix[i] else neg(Box(reset,neg(translated)))
            for w in W:
                assert evaluate(translated,w)==expected
                cases+=1
    print(f'PASS: {cases} QBF translation/world checks, with initial-state independence.')


def check_literal_lift():
    from check_variation import Model, disj as raw_or, neg as raw_not
    sizes=(2,3,2)
    old=tuple(product(*(range(d) for d in sizes)))
    lifted=tuple(product(*(range(2*d) for d in sizes)))
    projection=lambda w: tuple(a//2 for a in w)
    data={p:{w for w in old if rng.randrange(2)} for p in ('a','b')}
    atoms={p:(set(range(3)),{w for w in lifted if projection(w) in truth}) for p,truth in data.items()}
    for i in range(3):
        atoms[f'q{i}']=({i},{w for w in lifted if w[i]%2})
        assert atoms[f'q{i}'][1] and set(lifted)-atoms[f'q{i}'][1]
    model=Model([range(2*d) for d in sizes],atoms)
    literal={}
    for i in range(3):
        for w in lifted:
            positive=model.select(w,f'q{i}')
            negative=model.select(w,raw_not(f'q{i}'))
            assert positive and negative and not positive & negative
            union=positive|negative
            assert {projection(v) for v in union} == {v for v in old if all(v[j]==projection(w)[j] for j in range(3) if j!=i)}
            literal[i,w]=positive,negative
    formulas=['a','b']
    for _ in range(70):
        op=rng.choice(('not','and','modal'))
        if op=='not': formulas.append((op,rng.choice(formulas)))
        elif op=='and': formulas.append((op,rng.choice(formulas),rng.choice(formulas)))
        else: formulas.append((op,rng.randrange(3),rng.choice(formulas)))
    @lru_cache(None)
    def modal(phi,w):
        if isinstance(phi,str): return w in data[phi]
        if phi[0]=='not': return not modal(phi[1],w)
        if phi[0]=='and': return modal(phi[1],w) and modal(phi[2],w)
        i=phi[1]
        return all(modal(phi[2],v) for v in old if all(w[j]==v[j] for j in range(3) if j!=i))
    @lru_cache(None)
    def branch_translation(phi,w):
        if isinstance(phi,str): return w in atoms[phi][1]
        if phi[0]=='not': return not branch_translation(phi[1],w)
        if phi[0]=='and': return branch_translation(phi[1],w) and branch_translation(phi[2],w)
        positive,negative=literal[phi[1],w]
        return all(branch_translation(phi[2],v) for v in positive) and all(branch_translation(phi[2],v) for v in negative)
    cases=0
    for phi,w in product(formulas,lifted):
        assert branch_translation(phi,w)==modal(phi,projection(w))
        cases+=1
    print(f'PASS: {cases} nontrivial literal-branch lift checks on 96 worlds; each marker has a genuinely relevant singleton support.')


def check_positive_disjunction_qbf():
    """QBF hardness witness: only positive two-coordinate disjunctions intervene."""
    global N, W
    old_n, old_w = N, W
    N = 6
    W = tuple(product((0, 1), repeat=N))
    rng = random.Random(123)
    def matrix(depth):
        if not depth or rng.random() < .2: return rng.randrange(3)
        op = rng.choice(('not', 'and', 'or'))
        return neg(matrix(depth-1)) if op == 'not' else (op, matrix(depth-1), matrix(depth-1))
    def rename(a):
        if isinstance(a, int): return 2*a
        return (a[0], *(rename(b) for b in a[1:]))
    def translate(prefix, a):
        result = rename(a)
        for i, quantifier in reversed(list(enumerate(prefix))):
            p, q = 2*i, 2*i+1
            xor = Or(And(p, neg(q)), And(neg(p), q))
            guard = Or(neg(xor), result) if quantifier == 'A' else neg(And(xor, result))
            result = Box(Or(p, q), guard)
            if quantifier == 'E': result = neg(result)
        return result
    def qbf(prefix, a, valuation=()):
        if not prefix: return evaluate(a, valuation)
        values = [qbf(prefix[1:], a, valuation+(b,)) for b in (0, 1)]
        return all(values) if prefix[0] == 'A' else any(values)
    count = 0
    for a in [matrix(4) for _ in range(30)]:
        for prefix in product('AE', repeat=3):
            assert qbf(prefix, a) == evaluate(translate(prefix, a), (0,)*6), (prefix, a)
            count += 1
    N, W = old_n, old_w
    makers.cache_clear()
    select.cache_clear()
    print(f'PASS: {count} three-variable QBF translations using only positive pair-disjunction antecedents.')
    return count


if __name__=='__main__':
    main()
    check_qbf()
    check_literal_lift()
    check_positive_disjunction_qbf()
