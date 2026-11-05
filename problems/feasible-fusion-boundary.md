# Feasibility can hide simultaneous intervention effects

The full-product quotient has a sharp limitation: atomic intervention
relations need not determine simultaneous raw interventions on a feasible
subset. This note proves an unbounded-width separation with Boolean raw
coordinates, pairwise equality constraints, available literals, and
inclusion-minimal predicate supports. It also gives a finite criterion for
when Boolean assignment abstraction remains exact on such subsets.

The result concerns **raw support fusion**, not a new causal semantics.
The hidden-block gadget is a classical secret-sharing construction for
the complementary access structure. The intervention-specific results
are its masked realization, an atomic-isomorphic full-product comparison,
sharp size bounds in the equality/disjoint-support class, and precise
observation-width limits. Section 5 gives theorem-level comparisons;
publication priority of this combined result remains unestablished.

The companion [deterministic-fusion representation](deterministic-fusion-representation.md)
classifies all equality-only models with disjoint supports and deterministic
available literals. It also proves a sharp affine alternative: complete
bipartite coalition families can require exponentially fewer worlds when
general parity constraints replace coordinate equalities. This identifies
a precise boundary of the equality-only optimum below.

## 1. Language and observations

Let W be a nonempty finite subset of a finite coordinate product. A writable
feature predicate p has support S_p and truth local to that support. For a
coordinate set S put

    w E_S v  iff  w and v agree outside S.

The raw endpoint set for a consistent literal conjunction t, writing bits
b on its feature set J, is

    R_t(w) = {v in W : w E_(union_{p in J} S_p) v and v satisfies t}.   (1)

Normal antecedents use the exact bilateral verifier recursion, including
the left, right, and compatible-fusion alternatives at disjunctions.
Consequents may nest arbitrarily. They may also observe read-only decision
atoms d, which never occur in intervention antecedents. In particular,
calling d an output does not make it an independently writable feature.

Concretely, after exact negation normalization, a literal contributes its
one-literal branch, conjunction takes pairwise branch unions, and
disjunction retains both branch families and their pairwise unions.
Contradictory branches have no endpoints. This syntax-sensitive expansion
gives the union of the branch relations in (1); classical absorption such
as p OR (p AND q) = p must not be used to delete a fusion branch.

The **atomic reduct** retains W, all feature and decision truth labels,
and every positive/negative feature-literal endpoint relation. It forgets
the coordinate presentation and all composite intervention relations.

A support is **inclusion-minimal** if no proper subset supports that
predicate on W. This does not assert uniqueness of a minimal support:
equality-constrained coordinates can substitute for one another.

## 2. Arbitrary coalitions can unlock a decision

**Theorem 1 (coalition realization and atomic non-identifiability).**
Let H be a nonempty antichain of subsets of {1,...,n}, each of size at least
two. There are two finite raw models M_H and G_H such that:

1. All coordinates are Boolean. Each feasible domain is exactly the set
   of solutions of pairwise coordinate equalities; G_H is a full product.
   The writable feature supports are
   pairwise disjoint, local and inclusion-minimal, and both literals are
   available at every world.
2. The models have isomorphic atomic reducts, including a read-only
   decision atom d. Their feature projection h(w)=(p_1(w),...,p_n(w))
   preserves the endpoint images of every normal antecedent exactly as
   Boolean constant assignment.
3. In M_H, from every source w, a consistent intervention t assigning an
   arbitrary bit pattern to J has an endpoint with d(v) != d(w) exactly
   when some C in H is contained in J. In G_H no such intervention changes
   d. Thus H is exactly the family of minimal coalitions that can change d
   in M_H, despite identical complete single-feature intervention data.

**Construction and proof.** For each i take a raw bit a_i. For each C in H
take bits x_(C,i), i in C, constrained to be equal; write h_C for their
common value. No other feasibility restrictions are imposed. These
equalities can be imposed along a tree within each C, so all constraints
are binary. Define

    p_i = a_i XOR (XOR_{C containing i} h_C),
    S_i = {a_i} union {x_(C,i) : C contains i},
    d   = XOR_{C in H} h_C.

Give the read-only d one representative x_(C,i_C) from each equality
block as its support.
The worlds are in bijection with the free bits (a_1,...,a_n,(h_C)_{C in H}).
Every stated support is local. Deleting a_i from S_i fails because a_i can
be toggled alone. Deleting x_(C,i) fails because the entire C block can be
toggled with a_i and all the other coordinates of S_i fixed; this changes
p_i. Hence S_i is inclusion-minimal. The same argument proves minimality
of d's representative support.

Under a fused intervention on J, the block h_C is free to change precisely
when C is contained in J. Otherwise at least one x_(C,i), i outside J, is
fixed, and equality pins the entire block. A raw bit a_i is free precisely
when i is in J. Consequently every endpoint is obtained by choosing the
new bits of the released blocks arbitrarily and, for each assigned i,
setting

    a_i = b_i XOR (XOR_{C containing i} new_h_C).                 (2)

For unassigned i, no released block contains i, so p_i remains unchanged.
There are exactly 2^r endpoints, where r counts the C in H contained in J.
All have feature image h(w)[b]. Every assignment is therefore feasible.
Decision d can change iff r>0: flip one released block, keeping the others
fixed. The antichain condition makes the minimal changing coalitions
exactly H. Branchwise use of (1) extends the feature-image assertion to
all normal exact antecedents, not merely conjunctions.

For G_H instead take the full Boolean product on coordinates
(b_1,...,b_n,(h_C)), put p_i=b_i with support {b_i}, and d=XOR_C h_C
with its hidden-coordinate support. The map

    w |-> (p_1(w),...,p_n(w),(h_C(w)))

is a bijection preserving all labels. In both models a literal intervention
sets exactly one feature bit and fixes every h_C, since |C|>=2. Thus the
map is an atomic-reduct isomorphism. Every fused intervention of G_H still
fixes all hidden coordinates and d. Its supports are inclusion-minimal.
This proves all claims. QED.

M_H has n+sum_C |C| raw coordinates and 2^(n+|H|) worlds; G_H has
n+|H| raw coordinates and the same world count. If a common raw support
presentation is desired, the original alternative is to add guards
z_C=h_C outside every writable support of M_H. Extending worlds by these
unique guards gives another atomic-isomorphic comparison model with no
decision-changing fusion.

An antichain is necessary to specify an exact family of inclusion-minimal
coalitions. Excluding singletons is necessary for this comparison with a
model whose atomic interventions all preserve d. "Can change" is
existential: M_H always also has an endpoint with the old decision. It
therefore does not provide guaranteed successful recourse.

### Optimal size and the structure of equality constraints

**Theorem 2 (sharp size bounds).** Suppose W is exactly all solutions of
Boolean coordinate equalities, writable supports S_1,...,S_n are disjoint,
and both feature literals are available at every world. If the globally
minimal decision-changing coalitions are H, with all |C|>=2, then

    |W| >= 2^(n+|H|),
    number of raw coordinates >= n + sum_(C in H) |C|,
    |S_i| >= 1 + number of C in H containing i.

"Globally changing" means from some source under some sign assignment.
Thus the bounds need neither support minimality nor Theorem 1's stronger
every-source/all-sign requirement. M_H attains all three simultaneously.

**Proof.** Coordinate equalities partition the coordinates into classes B;
W is the unrestricted cube on their common bits. A class is *essential*
for d if toggling its bit changes d in some context. For any raw support U,
d varies along E_U somewhere iff U contains an essential class. In one
direction toggle that class; in the other connect the two endpoints by
single-class toggles, one of which must change d.

For each class B contained in the total writable support put
C_B={i:B intersects S_i}. Disjointness implies

    B is released by J iff C_B is contained in J.

Consequently the minimal global decision-changing coalitions are exactly
min_subset {C_B:B is fully covered and essential for d}. There is no
additional sign restriction: choose the target signs to be those of the
changing endpoint. Each C in H therefore requires a distinct essential
class B_C meeting all |C| owners. Each feature i additionally needs a
class wholly contained in S_i; otherwise E_S_i is identity and both
literals cannot be available. These n private classes are distinct and
are not any B_C. Counting classes, their coordinates, and their incidences
with S_i gives the three bounds. QED.

The hidden-class count is the familiar irredundant monotone-CNF counting
mechanism behind replicated-share constructions. The additional private
classes come from intervention availability. The bounds concern this
equality-support architecture, not unrestricted secret-sharing schemes.

The bounds remain valid if disjointness is replaced by inclusion-minimal
supports and exact Boolean feature projection for all conjunctions.
Indeed a minimal support contains at most one representative per equality
class and its predicate depends essentially on each represented class.
If a coordinate of a fully covered class belonged to two supports, all
supports other than either one would still cover that class. They could
change its bit and hence that unassigned feature, contradicting exact
projection. Thus fully releasable classes have exclusive owners, which
is all the counting proof needs. This weakening does not cover arbitrary
feasibility constraints, non-Boolean domains, or nonminimal overlaps.

At the minimum world count, Theorem 1's stronger uniform property forces
parity. There are exactly n private class bits a_i and |H| shared bits h_C.
Locality and availability give p_i=a_i XOR g_i((h_C)_(i in C)). No singleton
changes d, so d is independent of the private bits. Intervention on a
minimal C releases only h_C among shared bits. Changing d from every
source therefore forces every h_C toggle to flip d in every context.
Hence d=constant XOR XOR_C h_C. Minimal supports further require each g_i
to depend essentially on every incident shared bit. Parity of the decision
is forced at this minimum; parity of the feature masks is not.

### Exact observation language and first distinguishing width

For k>=1 let L_k have formulas and programs generated by

    phi ::= p | d | NOT phi | (phi AND phi) | [pi]phi
    pi  ::= act(A) | ?phi | (pi;pi) | (pi UNION pi) | pi*
             | converse(pi) | (pi INTERSECT pi).

Each primitive act(A) is a normal exact antecedent mentioning at most k
distinct writable features. It has relation R_A. Tests, sequence, choice,
iteration, converse, and intersection have their ordinary relational
meanings. Formula and test nesting and program length are unrestricted;
the width bound applies separately to each act(A), not to their total
vocabulary. Decision atoms occur only in observations/tests. In particular,
no raw fusion operation on programs or footprint-reading test is supplied.

**Theorem 3 (exact distinguishing width).** For Theorem 1's pair, let
rho=min_(C in H)|C|. The world bijection preserves every L_k formula and
program relation for k<rho. The first possible distinguishing width is
exactly rho. This includes arbitrary-depth conditionals and adaptive
relational experimentation, not just a bounded number of literal tests.

**Proof.** Every exact branch of a width-k antecedent has at most k
features. If k<rho it releases no shared block; its entire endpoint relation
agrees in both models. Mutual structural induction preserves formula truth
and program relations, including tests; iteration is preserved because all
finite paths correspond. For C in H of size rho and any signs b, let t
assign b on C. At a source with d=0, [act(t)] NOT d holds in G_H but fails
in M_H. At a source with d=1 use [act(t)]d. These witnesses have width rho.
QED.

Thus there is no uniform definition of raw fusion in the endpoint-only
atomic language L_1. This is an isomorphism argument, not a new invariance
principle. It does not exclude syntax-aware compilation with auxiliary
variables or enriched states; DL-PPA already has such translations.
For each k, H={{1,...,k+1}} gives the strict k versus k+1 hierarchy.

A more precise extension retains the blocks for any subfamily H_0 of H
and guards the others. It agrees with M_H on every antecedent whose
branches contain no C in H\H_0. If H\H_0 is nonempty, the first
separating width is min_(C in H\H_0)|C|: at such a C no member of H_0
is contained in C, by antichainness. Choosing H_0 to contain all coalitions
of size at most k exhibits the undetermined higher-order part even after
complete width-k data are supplied.

### What full products restore

On a full product, E_(S union T)=E_S composed E_T. For a conjunction t on
J, sequentially execute the resets R_p union R_NOT-p for p in J, then test
t. This relational program has exactly R_t as its endpoint relation.
The equality can fail on feasible subsets: in Theorem 1 every atomic
reset fixes the h_C, while a fused support may release an entire block.
Thus the obstruction is a loss of the support-union composition identity,
not merely coarse observations or classical equivalence of antecedents.

### First distinguishability is not complete reconstruction

For a fixed J let F_(J,k) be the reflexive-transitive closure of the union
of E_(union_(i in K)S_i) over K contained in J with |K|<=k. Each generating
reset is observable from width-k data: take the program choice of all
signed conjunctions on K. All such paths remain in E_(union_(i in J)S_i).

**Reset-connectivity criterion.** Every raw conjunction on J is recoverable
by such resets followed by its target test iff

    F_(J,k) = E_(union_(i in J)S_i).                              (2a)

Sufficiency is the displayed reset program followed by the test. For
necessity, if a pair (w,v) lies in the right side but not the left, set the
target signs to the feature values of v. This conjunction reaches v;
no program using only these resets, tests, sequence, choice, iteration,
converse and intersection can escape the F_(J,k) component. The criterion
is for these J-local endpoint programs, not arbitrary oracle tests or
footprint-aware parallel operators. It is an elementary relational
connectivity fact, not a new dynamic-logic principle.

For M_H the smallest k making (2a) true for every J is

    k_reconstruct = max_(C in H)|C|,

whereas the first width distinguishing M_H from G_H is min_C|C|. To see
sufficiency, change private bits one at a time and each released h_C by a
reset on C; these moves reach every permitted endpoint. For necessity,
a block with |C|>k is fixed by every width-k intervention, even using all
features and arbitrarily many steps, but a reset on C can flip it. Thus
these two width thresholds answer different questions. For G_H all joint
relations are already reconstructed at width one. Having identical atomic
data does not identify even which reconstruction threshold applies.

## 3. An exact quotient test without the product hypothesis

Now let P be precisely the writable feature vocabulary; decision atoms are
handled in Section 4. Write Q_P for the full Boolean assignment model and
h(w)(p)=p(w). Define T_q=union_{p in P, p!=q} S_p. Two finite conditions are:

- **Availability:** both literal endpoint sets are nonempty at every w.
- **Maximal frame test:** q is invariant under E_T_q for every q in P.

The second is a functional dependency: agreement outside T_q determines q.
It is an established dependence notion, not a new independence definition.

**Theorem 4 (maximal-support criterion).** For any nonempty finite feasible
W with local feature predicates, the following are equivalent:

(i) Availability and the maximal frame tests hold.

(ii) For every normal exact antecedent A and every w,

    h[R_A(w)] = R_A^(Q_P)(h(w)).                                (3)

It suffices in (ii) to test literals and, for each q, all signed conjunctions
of the other feature names. Under either condition h is onto Q_P and
preserves every formula of the base nested conditional language over P.

**Proof.** Suppose (i). An endpoint of a conjunction assigning J has its
prescribed bits. For q outside J its support union is contained in T_q,
so the maximal frame test preserves q. Its projected endpoint is therefore
exactly h(w)[b]. To show nonemptiness, apply the requested literals one at
a time. Availability supplies each step; the maximal tests imply atomic
noninterference, so earlier assignments remain true. The resulting world
agrees with w outside the union of assigned supports and hence satisfies
(1). Splitting arbitrary exact antecedents into their literal-conjunction
branches establishes (3). This splitting keeps the inclusive fusion
branches and is not classical DNF replacement.

Conversely, (3) for literals implies availability. If w E_T_q v, assign
every feature other than q its value at v. Then v is an endpoint of that
conjunction, so its correct projected image forces q(v)=q(w). If P={q},
T_q is empty and the conclusion is automatic. Thus the restricted tests
already imply (i). Sequentially setting all features proves surjectivity;
induction on formulas using (3) proves nested truth preservation. QED.

This quotient claim is not a claim about all of L_k's program operations.
Unlike the isomorphism in Theorem 3, endpoint-image equality need not
preserve intersection. For example, take W={(r,c) in Z_4^2:c=r or c=r+1},
p=c mod 2 with support {c}, and q=r mod 2 with support {r}. Both tests of
Theorem 4 hold. From (0,0), p:=1;q:=1 reaches (1,1), while q:=1;p:=1
reaches (3,3). Their intersection is empty in W but nonempty in the Boolean
quotient. Thus arbitrary nesting of primitive conditionals is preserved,
while importing the richer observation language requires separate proof.

Although the equivalent conjunction test has exponentially many signs,
the semantic criterion has only |P| maximal frame tests and |P| availability
tests. For an explicitly listed W they can be checked by grouping rows by
coordinates outside S_p or T_q, respectively. Availability asks for both
p bits in each first group; a frame test asks for a constant q bit in each
second group. A direct pairwise implementation is polynomial in the
explicit table size. This does not claim efficient recognition from a
succinct circuit or an unknown classifier.

If the quotient fails, a failed literal or a conjunction of at most |P|-1
other features witnesses it. On full products, the maximal tests follow
from the atomic tests by the support-union composition identity, recovering
the earlier [Boolean quotient theorem](visible-boolean-quotient.md).

**Proposition 5 (the witness-width bound is optimal).** For every m>=3
there is a feasible raw model on m writable features in which every
antecedent mentioning fewer than m-1 features has exactly the Boolean
endpoint images, but a conjunction of m-1 features does not. All literals
are available, all supports are inclusion-minimal, and feasibility uses
only Boolean coordinates and pairwise equalities.

**Proof.** Put n=m-1. Use one equality block x_1=...=x_n=h, free bits
a_1,...,a_n,c, and feature predicates

    p_i=a_i XOR h, with support {a_i,x_i},
    q=c XOR h,     with support {c,x_1}.

Every support is local and inclusion-minimal. Fewer than n feature supports
cannot cover all x_i: x_2,...,x_n each require their respective p_i, and
x_1 requires p_1 or q. Thus h stays fixed, assigned a_i or c realize the
requested bits uniquely, and all unassigned features retain their values.
Exact branch expansion proves the statement for all smaller-width normal
antecedents. Intervening jointly on p_1,...,p_n frees h while c is fixed;
choosing the flipped h and appropriate a_i changes the unassigned q. QED.

This is a feature-quotient lower bound, distinct from Theorem 3's
read-only-decision hierarchy. Its supports need not all be disjoint:
S_q and S_p_1 share x_1. Theorem 1's disjointness claim concerns that
theorem's writable features, not this separate optimal-bound example.

## 4. Classifier outputs must be observations, not extra assignments

Suppose the feature criterion holds and a given deterministic raw classifier
is observed through decision atoms D. There exists a feature-only classifier
f:{0,1}^P -> {0,1}^D such that d(w)=f(h(w)) exactly when

    h(w)=h(v) implies d(w)=d(v).                                (4)

This is the familiar functional dependence P -> D. Surjectivity makes f
total and unique. If (4) holds, (3) and induction preserve all formulas of the base nested
conditional language whose antecedents use P and whose consequents may observe D, with
target decisions recomputed as f after each assignment. This gives a
faithful feature-only intervention explanation of the supplied classifier.
It does not assert that d stays fixed under feature interventions.

If (4) fails, no feature-only deterministic classifier preserves even the
observed output at every world. One must retain additional state or use a
set-valued abstraction. Theorem 1 goes further: even retaining the decision
label and every single-feature transition does not determine the output
of compound raw interventions. A coarse-predicate explanation can miss
jointly released raw degrees of freedom, despite perfectly faithful
Boolean behavior of all feature predicates themselves.

### A common frame test for feature and decision effects

Assume literal availability and atomic noninterference between writable
features. Let o be an observed Boolean predicate, and let I be a set of
feature names whose atomic resets all preserve o. This covers a feature
q with I=P\{q}, or a read-only decision d with I=P when all singleton
experiments preserve d. Write S_J=union_(i in J) S_i.

**Proposition 6 (decision spectrum and exact first-effect width).** For
J contained in I, every assignment b on J and every source w satisfy

    {o(v):v in R_(J:=b)(w)} = {o(v):w E_S_J v}.                  (5)

Hence o is preserved by every intervention using I iff it is invariant
under E_S_I. If preservation fails, its exact least intervention width is

    min {|J|: J contained in I, some w E_S_J v have o(w)!=o(v)}.  (6)

All assignments on such a J have the same decision spectrum at a given
source. In particular, its inclusion-minimal globally changing coalitions
are independent of the requested signs. The test on the right is exactly
the functional dependency "coordinates outside S_J determine o".

**Proof.** Inclusion from left to right is immediate. Given v in E_S_J(w),
sequentially assign the requested feature literals starting at v. Each
step exists, preserves o and earlier assigned feature bits, and changes
only coordinates in S_J. The final endpoint is in R_(J:=b)(w) and has
o(v). This proves (5); taking J=I and then minimizing gives the rest. The
same sequence started at w always supplies an endpoint with o(w), so
possible change is never guaranteed change under these hypotheses. QED.

For features this recovers the maximal-support criterion and its optimal
m-1 witness bound. For read-only decisions the bound becomes n and is
attained by H={{1,...,n}}. It unifies the two tests without confusing them:
feature quotient exactness may hold while every higher-order decision
coalition in H remains hidden from atomic experiments. Equations (5)-(6)
are criteria for a supplied raw presentation, not ways to infer its
unobserved support unions from an atomic reduct.

### Two explicit XAI instances

For two coarse features take raw coordinates (a_1,a_2,x_1,x_2), constrain
x_1=x_2=h, set p_i=a_i XOR h, and let the deterministic raw classifier be
d=h. Supports are {a_1,x_1} and {a_2,x_2}. From raw (0,0,0,0), the p_1:=1
experiment has the unique endpoint (1,0,0,0), with observed (p_1,p_2,d)
=(1,0,0); p_2:=1 similarly yields (0,1,0). The joint assignment p_1=p_2=1
has exactly two endpoints:

    (1,1,0,0), with observed (1,1,0);
    (0,0,1,1), with observed (1,1,1).

The product comparison has raw (p_1,p_2,h), singleton feature supports and
the same d=h. It has the identical labeled state/atomic-transition system,
but the joint assignment from (0,0,0) has only (1,1,0). Thus every
single-feature experiment at every state is known, and reconstructs the
visible feature assignment, yet possible joint decision change differs.
The classifier is deterministic on raw inputs; nondeterminism comes from
intervening on coarse features. It is not a classifier determined by only
(p_1,p_2), and it is not a guarantee of beneficial recourse.

For unequal thresholds take H={{1,2},{2,3,4}}. The construction has six
independent bits, 64 worlds, nine raw coordinates, and supports of sizes
2,3,2,2; all these sizes are optimal by Theorem 2. Its minimal changing
coalitions are exactly the pair {1,2} and the triple {2,3,4}. Guarding only
the triple block preserves every width-two endpoint relation and all
L_2 observations, including the known pair effect, while removing the
triple effect. Full reconstruction needs width three. This illustrates
why observing one successful joint explanation does not identify all
minimal explanations.

These are representation and non-identifiability statements for a specified
intervention semantics. They do not infer causal effects from observational
data, classify decidability of every feasible-domain language, or settle
Briggs's general import-export question.

## 5. Precise relation to prior work

The theorem isolates a raw-fusion realization and non-identifiability result;
none of the following broader ideas is claimed as new.

- **Secret sharing and arbitrary coalitions.** Ito, Saito and Nishizeki,
  *Secret Sharing Scheme Realizing General Access Structure* (1987),
  Proposition 1 and Theorem 1, pp.99-100, realize arbitrary upward-closed
  access structures. Benaloh and Leichter, *Generalized Secret Sharing
  and Monotone Functions* (CRYPTO '88 proceedings, 1990), definitions on
  pp.29,31 and Theorem 2 on p.32, construct secret-sharing schemes for
  any monotone formula with secrets in Z_m. Their AND operation splits a
  secret additively; OR replicates shares. The hidden gadget here is
  exactly this construction for the complementary access structure:
  observers K receiving their incident copied shares determine d iff
  K meets every C in H, represented by
  AND_(C in H) OR_(i in C) v_i. With m=2 the clause shares are h_C and
  d=XOR_C h_C. A writable complement J can flip d iff it contains some C.
  Feature masks a_i do not reveal missing shares, since they are free.
  Arbitrary coalition realization alone is therefore not new. The extra
  results here concern primitive intervention relations, full-product
  comparison, minimal supports, sharp size under the stated restrictions,
  and arbitrary-depth observation width; no unrestricted secret-sharing
  optimality claim is made.
  [Ito-Saito-Nishizeki](https://archiv.infsec.ethz.ch/education/as09/secsem/papers/ItSaNi87.pdf),
  [Benaloh-Leichter](https://www.cs.cornell.edu/courses/cs754/2001fa/bena88.pdf).
- **Functional dependence and high-order failure.** The maximal frame tests
  and (4) are functional dependencies. Kontinen, Link and Vaananen,
  *Independence in Database Relations* (WoLLIC 2013), proof of Theorem 1,
  pp.186-187, already use a Boolean parity relation with full proper
  projections and a failing higher-order independence claim. Their
  Theorem 5, p.192, constructs Armstrong relations realizing exactly the
  implied independence atoms. Our width result is not a discovery of high-order dependence: its extra content is
  the pair of equal-atomic-reduct raw intervention models, with minimal
  supports, and realization of any specified minimal coalition family.
  [Primary text](https://www.mv.helsinki.fi/home/jvaanane/KonLinVaa.pdf).
- **Classifier logic.** Xinghan Liu and Emiliano Lorini, *A unified logical
  framework for explanations in classifier systems* (2023), Definitions
  1-2, give feasible feature states and outputs determined by a fixed
  classifier; Definition 4 and Proposition 2 identify definiteness with
  functional dependence. Numbering here follows the
  [versioned author text](https://arxiv.org/pdf/2105.14452v8);
  [publication](https://doi.org/10.1093/logcom/exac102). Outputs are read-only
  in their base language, not throughout all later dynamic extensions.
  Section 4 uses that established distinction; our negative result concerns
  support fusion not determined by the complete atomic intervention reduct.
- **Causal abstraction.** Beckers and Halpern (2019), Definition 3.12,
  define the intervention map by equality of cylinder images. Definitions
  3.13-3.14 add outcome compatibility, surjectivity and all high-level
  interventions; Definition 3.17 imposes a partition-based construction; Example 3.16 already
  warns that overlapping macro-observables can constrain which simultaneous
  interventions make sense. Geiger et al. (2025), Definition 25, explicitly
  compare images of solution sets under interventions. Equation (3) is a
  specialized exact-abstraction requirement, not a new general one.
  [Beckers-Halpern text](https://www.cs.cornell.edu/home/halpern/papers/abstraction.pdf),
  [Geiger et al. text](https://www.jmlr.org/papers/volume26/23-0058/23-0058.pdf).
- **Constrained causal models.** Beckers, Halpern and Hitchcock, *Causal
  Models with Constraints* (2023), unnumbered definitions in Sections 2-3,
  pp.3-5, allow feasibility constraints and disconnection of structural
  equations; Theorem 2, p.10, axiomatizes their fixed-signature L_d. Section 2 permits equationless endogenous
  variables and interventions that add their missing equations. Our raw
  conjunction endpoints can be encoded in their language: an exogenous U
  has range W; raw X_i have equations X_i=projection_i(U); visible Y_p have
  no equations; constraints require X in W and Y_p=p(X). At context U=w,
  disconnect the union of the assigned
  supports and set the corresponding Y_p bits. The resulting X-solutions
  are exactly (1). This is a context-indexed, one-step representation,
  deduced from their definitions, not their stated theorem or a
  compositional translation of our nested conditional language. Their
  displayed L_d language has Boolean postconditions and a fixed exogenous
  context. Our theorem concerns information lost at the smaller atomic
  observation interface, not the invention of constrained interventions.
  [Proceedings text](https://proceedings.mlr.press/v213/beckers23a/beckers23a.pdf).
- **Dynamic assignment.** Herzig, Maris and Vianey (IJCAI 2019), Section
  2.2, already show that programs with identical binary endpoint relations
  may differ in parallel composition: writing p to its existing value and
  skip have different write footprints. Boudou, Herzig and Troquard,
  *Resource separation in dynamic logic of propositional assignments*
  (2021), pp.2-3, similarly motivate writability information. Generic failure of
  endpoint-only parallel reconstruction is therefore already present.
  The particular result here adds identical *primitive literal* relations,
  disjoint inclusion-minimal supports, equality-only feasible domains, and
  arbitrary minimal decision-changing coalitions. Theorem 3 does not
  contradict DL-PPA's instrumented translation into DL-PA (2019, Section
  3, Proposition 7 for correctness and Proposition 8 for polynomial size),
  which introduces copied variables and write flags. DL-PPA Proposition 3
  sequentializes parallel programs with disjoint entire occurring-variable
  sets, not merely disjoint writable supports on constrained domains.
  [DL-PPA](https://www.ijcai.org/proceedings/2019/0774.pdf),
  [2021 text](https://arxiv.org/pdf/2104.14884).

The inspected source statements do not directly state the combined
masked equal-reduct theorem or its size and observation-width refinements.
This bounded comparison does not establish publication priority. The
intervention-specific package, rather than the inherited secret-sharing
gadget or assignment calculus, is the remaining candidate contribution.

## Verification

Run `python models/check_feasible_fusion.py`. It independently enumerates
coordinate endpoints, tests the maximal criterion on small feasible models,
checks minimal supports and all coalition/bit-pattern endpoints in the
realization construction, compares product and guarded atomic reducts,
checks the equality-class characterization and size rigidity, and exercises
nested formulas and a nonconstant read-only classifier. Finite checks
support the general proofs; they neither prove priority nor replace them.


