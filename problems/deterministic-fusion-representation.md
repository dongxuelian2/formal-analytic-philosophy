# A representation theorem for deterministic atomic interventions

The [coalition theorem](feasible-fusion-boundary.md) constructs equality-only
models whose complete atomic intervention data conceal arbitrary joint
effects. Here that construction is extended to a classification of the
whole equality-only class with deterministic available literals. Endpoint
counts determine its feature-labeled fusion structure. A sharp affine
comparison then shows exactly why the equality-only size bounds cannot
be extended to general linear constraints.

The proofs use elementary coordinate decomposition, Boolean-lattice
Mobius inversion, and a forest-independence argument. The underlying
secret-sharing constructions are classical; see the attribution below.
No publication-priority claim is made.

## 1. Equality models have a complete normal form

Let W be exactly the Boolean solutions of pairwise coordinate equalities.
Let S_1,...,S_n be pairwise disjoint supports of local Boolean features
p_1,...,p_n. For J contained in [n] and target bits b define

    R_(J:=b)(w) = {v in W: v agrees with w outside S_J,
                          p_i(v)=b_i for i in J},
    S_J = union_(i in J) S_i.

The empty assignment is the identity. Call atomic interventions
**deterministic and available** when |R_(i:=b)(w)|=1 for every i,b,w.
Read-only output labels may be arbitrary functions on W.

**Theorem 1 (equality normal form).** Under these hypotheses there are
n private equality-class bits a_i and m remaining bits h_t such that:

1. Feature p_i has the form a_i XOR g_i(h). Its mask g_i depends only on
   remaining equality classes meeting S_i.
2. Each remaining class is either guarded (not contained in S_[n]) or
   has an owner set C_t={i: its class meets S_i} of size at least two.
3. The bijection w -> (p(w),h(w)) sends every signed conjunction to

       p' = p[J:=b],
       h'_t arbitrary if C_t is contained in J,
       h'_t = h_t otherwise, including every guarded t.          (1)

Thus every model in this class has an atomic-isomorphic full-product
comparison with singleton feature supports: on coordinates (p,h), keep
the transformed output labels and allow primitive interventions to set
only p_i. In the original model, (1) describes precisely the additional
joint freedom. Any output invariant under all atomic interventions is
exactly a function of h.

Support minimality is not needed. If it is imposed, each S_i contains
at most one representative per equality class, its private class is a
singleton raw coordinate, and its mask depends essentially on each
represented hidden class.

**Proof.** The equality classes are independent Boolean bits. The fiber
E_(S_i)(w) has size 2^k_i, where k_i counts classes wholly contained in S_i.
Its two truth-labeled parts are the two literal endpoint sets. Both are
singletons, so k_i=1. Denote that private class bit by a_i. Disjointness
makes these n private classes distinct. Every other class is fixed by
all atomic interventions. For each fixed hidden assignment, the two a_i
values must give opposite p_i values, proving the mask representation.

Locality excludes other private bits from p_i. A remaining fully covered
class has at least two owners and is released exactly when all its owners
belong to J. Every unassigned feature therefore retains its value. For
each choice of released hidden bits, set a_i=b_i XOR g_i(h') for assigned
i; this gives exactly one endpoint. This proves (1) and bijectivity.
Atomic invariance of an output is precisely independence of all a_i,
or equivalently of all p_i at fixed h. Finally, duplicate representatives
of a class in a support are redundant, and a represented inessential
class can be deleted. These observations prove the minimality assertions.
QED.

Branchwise union extends (1) to all normal exact antecedents, with the
inclusive fusion branches retained. The resulting isomorphisms preserve
the rich relational observation language of the coalition note, including
tests, iteration, converse and intersection. This is a bijective
representation, not the noninjective feature quotient discussed there.

Determinism alone does not imply support minimality: x=y=h,
S_1={a,x}, S_2={b,y}, p_1=a, p_2=b has redundant support coordinates but
still releases h jointly. Conversely availability and minimality do not
imply determinism: p=a AND b on the unrestricted two-bit cube with
support {a,b} has respectively three and one negative/positive endpoints.

## 2. Endpoint counts identify the feature-only fusion system

Write m_C for the number of hidden classes with owner set C, |C|>=2,
and m_infty for the number of guarded classes. Guarded ownership and
redundant copies are deliberately not recorded.

**Theorem 2 (count-profile representation).** In Theorem 1's class,
the count |R_(J:=b)(w)| is independent of w and b and equals 2^r(J), where

    r(J) = sum_(C contained in J, |C|>=2) m_C.                  (2)

Consequently

    m_C = sum_(J contained in C) (-1)^(|C|-|J|) r(J),
    m_infty = log_2 |W| - n - r([n]).                           (3)

A profile r on all subsets is realizable on 2^(n+m) worlds if and only if
r(empty)=r({i})=0, every coefficient in (3) for |C|>=2 is a nonnegative
integer, and sum_C m_C<=m, where m is a nonnegative integer.
Two models in this class, retaining feature truth labels but no additional
output labels, are isomorphic for all joint interventions if and only if
they have the same |W| and r. The least raw-coordinate and support sizes
for a prescribed signature are

    n + m_infty + sum_C |C| m_C,
    |S_i| = 1 + sum_(C containing i) m_C.                       (4)

These minima are attained simultaneously by inclusion-minimal supports.

**Proof.** Formula (1) gives (2). Boolean-lattice Mobius inversion gives
(3). For the converse, use one private bit per feature, one equality
block with one copy per owner for each of the m_C occurrences, and
m_infty single guarded coordinates outside all writable supports. Set
p_i to its private bit XOR the incident hidden bits. These supports are
minimal and realize (2). Any two models with the same multiplicities
have the same normal form after permuting hidden coordinates within
owner types; this preserves all feature labels and all relations (1).
Conversely an isomorphism preserves |W| and each endpoint count, so (3)
recovers the same signature. Every private or guarded class requires
at least one coordinate and every C-owned class at least |C| coordinates,
one in each disjoint support. This proves (4). QED.

Counts do not determine an arbitrary output labeling, a unique hidden
basis, the raw coordinate presentation, or the masks g_i. An unknown
structure having these counts need not belong to the equality class:
the theorem is a classification *within* the stated class, not a
cardinality-only test for an arbitrary relational system. It requires
all subset counts, not merely atomic observations. For such a model,
the complete reset-reconstruction width is max{|C|:m_C>0}, or one when
there are no released hidden classes. This is independent of which
blocks happen to affect a supplied decision label.

Power-of-two counts, monotonicity and even supermodularity of r are
insufficient. For n=3 the profile r(singletons)=0, r(pairs)=1, r([3])=2
has m_[3]=-1. It cannot occur in this equality class. Section 3 realizes
it using a single parity constraint, while retaining the other hypotheses.

## 3. A sharp boundary for affine feasibility

Here n>=2 and W is any nonempty affine subspace w_0+V of a Boolean coordinate
space. Supports are disjoint, all feature literals are available, and
a read-only Boolean d is preserved by every singleton intervention.
Neither feature predicates nor d are required to be affine functions.
Let G be the graph whose edges are the pairs that can change d from
some source under some target signs. Let c(G) count all connected
components, including isolated vertices. Higher-order minimal effects
are allowed as well.

**Theorem 3 (affine forest lower bound).** Put
P_i={v in V: support(v) is contained in S_i}, and q_i=dim P_i. Then

    dim V >= sum_i q_i + n - c(G) >= 2n - c(G).                 (5)

For every nonisolated vertex i, |S_i|>=q_i+1>=2. In particular, connected
G requires at least 2^(2n-1) worlds, 2n raw coordinates, and two
coordinates per feature support. Deterministic literals and minimal
supports are not needed for these lower bounds.

**Proof.** Availability forces q_i>=1. Disjointness makes
P=P_1 direct-sum ... direct-sum P_n. Every P_i translation stays within
an atomic reset fiber. Its target is an endpoint for one of the two
signs, so d is invariant under P_i and therefore under P.

For an edge ij choose source and endpoint with different decisions;
their difference v_ij belongs to V, is supported within S_i union S_j,
and is not in P. Its restriction to S_i is outside P_i: otherwise
subtracting that private vector leaves an element of P_j, contradicting
v_ij not in P. The same holds at j.

Choose a spanning forest of G. Its n-c(G) selected edge vectors are
independent modulo P. Indeed, in a putative combination lying in P,
a leaf's support isolates its sole incident edge restriction. That
restriction is outside P_i, so its coefficient must vanish. Delete the
edge and repeat. Dimension counting proves (5). At a nonisolated vertex,
P_i and an incident edge restriction span at least q_i+1 dimensions
inside the |S_i|-dimensional coordinate space, proving the support bound.
QED.

**Theorem 4 (optimal affine realization of complete bipartite effects).**
Partition [n]=A disjoint-union B, with |A|=k>=1, |B|=l>=1. There is a
model with exactly the cross pairs {i,j}, i in A, j in B, as its minimal
decision-changing coalitions, uniformly at every source and target
assignment. It has deterministic available literals, minimal disjoint
supports, 2^(2n-1) worlds, 2n raw coordinates and support size two.
All three sizes are optimal among the affine models of Theorem 3 with
this coalition family. Its atomic reduct has a full-product comparison
in which every joint intervention preserves d.

**Construction and proof.** Use private bits a_i and hidden bits x_i with

    XOR_(i=1)^n x_i = 0,
    S_i={a_i,x_i},   p_i=a_i XOR x_i,
    d=XOR_(i in A) x_i = XOR_(i in B) x_i.                      (6)

A singleton pins x_i by the outside parity constraint and uniquely
sets a_i. Each support is minimal: a_i can toggle alone; x_i can toggle
with some other x_j while keeping a_i fixed. For a nonempty J, the
permitted hidden differences are exactly the even-parity vectors
supported in J. For each such choice the target signs uniquely fix
the assigned a_i, and unassigned features stay fixed. Hence

    |R_(J:=b)(w)| = 2^(|J|-1) for J nonempty.                   (7)

The decision changes iff the difference has odd parity on A, which
requires and, by toggling one bit on each side, is possible exactly
when J meets both A and B. The unchanged hidden vector always gives
an endpoint with the old decision. Thus possible change is not
guaranteed recourse.

There are n free private bits and n-1 independent hidden bits. Taking
any basis of the hidden even-parity space gives the bijection to a full
product on (p,h). Both atomic systems set one p_i and fix h; the
comparison fixes h under every fusion. The graph K_(k,l) is connected,
so Theorem 3 proves all three optimalities. QED.

For the same cross-pair family, equality-only models need
2^(n+kl) worlds, n+2kl raw coordinates, and supports of size 1+l on A
and 1+k on B. The equality-to-affine optimum world-count ratio is therefore
2^((k-1)(l-1)). For k=l=2, equality models need 256 worlds and 12 raw
coordinates, whereas the affine optimum uses 128 worlds and 8 raw
coordinates. For balanced partitions the exponent gap is quadratic
in n. This is a quantitative boundary between two explicit model classes,
not a lower bound for arbitrary nonlinear feasibility or secret sharing.

**Corollary 5 (rigidity at the raw-coordinate minimum).** Under Theorem 3,
if G is connected and there are exactly 2n raw coordinates, then G is
complete multipartite. If every changing pair can change d from every
source, G must be complete bipartite. Both characterizations are sharp.
In particular, a connected graph that is not complete multipartite
requires strictly more than 2n raw coordinates in this affine class.

**Proof.** The support bounds force |S_i|=2, q_i=1 and no outside
coordinates. The forest bound gives dim V>=2n-1; equality dim V=2n
would make V the full raw space and q_i=2, a contradiction. Quotient
each two-dimensional support space by P_i. The image of V is a
dimension-(n-1) subspace H of F_2^n with no weight-one vector. Indeed,
a vector supported only at i in the quotient could be lifted and its
other private blocks subtracted, giving an additional direction in
P_i. A codimension-one binary subspace avoiding every unit vector is
exactly the even-parity space. Translate W first if it is affine rather
than linear. The decision descends to a Boolean function on H.

Declare i equivalent to j when d is invariant under translation
e_i+e_j. This is an equivalence relation: invariance under two
translations implies invariance under their sum. Pairs change d
somewhere exactly between different equivalence classes, proving the
complete-multipartite claim. Conversely, for any partition into at
least two parts, let d be one exactly when every part has even parity.
Same-part pair moves preserve it, while every cross-part pair changes
it at the zero vector. Construction (6) with this decision therefore
realizes every such graph at the minimum.

If changing pairs have an effect from every source, their unique
nonzero hidden pair direction flips d everywhere. Three distinct parts
would give directions e_i+e_j, e_j+e_k and their sum e_i+e_k all flipping
d, which is impossible: two flips compose to preservation. There are
therefore exactly two parts, and Theorem 4 attains this case. QED.

Uniformity matters. For n=3, on the hidden even-parity space, d=1
exactly at 000 has G=K_3 and attains both size bounds, but its pair
effects depend on the source. This is not the uniform bipartite case.

## 4. Attribution and verification

The inversion in (3) is the classical Boolean-lattice inversion formula,
not a new combinatorial principle; see Rota (1964), Section 3 and the
inclusion-exclusion corollary on p.345
([primary text](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/rota1.pdf)).

The hidden gadget (6) is also an instance of Benaloh--Leichter's
classical monotone-formula secret sharing: an observing coalition
determines d exactly when it contains all of A or all of B. Apply their
OR operation to the two AND clauses, sharing the same secret separately
as the sum of the A shares and of the B shares. This gives exactly the
parity equality in (6). Their definitions on p.31 and Theorem 2 on p.32
already supply this construction
([primary text](https://www.cs.cornell.edu/courses/cs754/2001fa/bena88.pdf)).
Thus formula-based compression over the replicated CNF construction is
not claimed as new. The results here add the intervention normal form,
the count-profile classification, and the sharp affine forest bound
including the private degrees of freedom forced by literal availability.

The broader connection between linear-code supports and secret-sharing
access structures is also established: Massey (1993), Section 3's
Proposition, characterizes the access structure by specified minimal
codewords of the dual code
([primary text](https://www.isiweb.ee.ethz.ch/papers/arch/mass-1993-3.pdf)).
The forest bound is proved directly above rather than attributed to
that proposition. These inspected statements do not establish priority
of the intervention-specific classification or bound.

Run `python models/check_deterministic_fusion.py`. Its direct coordinate
enumeration checks normal forms with nonlinear masks and redundant
representatives, profile inversion, the parity construction, and the
forest bound on exhaustive small linear subspaces and invariant decision
tables. Finite checks supplement the general proofs.
