# Feasibility can hide simultaneous intervention effects

The full-product quotient has a sharp limitation: atomic intervention
relations need not determine simultaneous raw interventions on a feasible
subset. This note proves an unbounded-width separation with Boolean raw
coordinates, pairwise equality constraints, available literals, and
inclusion-minimal predicate supports. It also gives a finite criterion for
when Boolean assignment abstraction remains exact on such subsets.

The result concerns **raw support fusion**, not a new causal semantics.
Read-only classifier observations and constrained causal models already
occur in the literature; Section 5 specifies the comparisons. Publication
novelty of the precise separation and criterion remains unestablished.

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

1. All coordinates are Boolean and feasibility is specified only by
   pairwise coordinate equalities. The writable feature supports are
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

Give d one representative x_(C,i_C) from each equality block as its support.
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

For G_H add a guard coordinate z_C=h_C for every C, and leave every z_C
outside every writable support S_i. Extend each world by its uniquely
determined guards. This is a bijection of world sets; predicate labels and
support minimality are preserved. Every fused intervention now fixes each
z_C and hence every h_C, so d never changes. Before adding guards, a
single-feature intervention already fixed every h_C because |C|>=2.
Therefore both models have exactly the same literal transitions under the
world bijection: each sets its one p_i bit while all h_C remain fixed.
This proves the atomic-reduct isomorphism and all claims. QED.

The construction is finite and explicit: M_H has n+sum_C |C| raw
coordinates and 2^(n+|H|) worlds. G_H has |H| extra coordinates but the
same number of worlds. An antichain is a convenient exact list of minimal
coalitions, not an assumption needed for the endpoint calculation.

### No reconstruction from atomic dynamics

**Corollary 2.** Simultaneous raw support fusion has no uniform elimination
into any language whose interpretation depends only on the atomic reduct.
In particular, it cannot be defined uniformly by ordinary relational
dynamic-logic programs built from feature-literal transitions using
sequence, choice, tests, and iteration, with tests in that same language.

**Proof.** Such languages have identical truth at corresponding worlds of
isomorphic atomic reducts. Take H={{1,...,n}} and t=p_1 AND ... AND p_n.
At any world with d=0, [t] NOT d is true in G_H and false in M_H. QED.

This is same-state, endpoint-only nondefinability. It does not exclude
syntax-aware compilation with auxiliary variables or enriched execution
states. DL-PPA already retains write footprints and can be compiled into
DL-PA using additional variables. The corollary states exactly which
information is insufficient: all primitive literal endpoint relations and
all decision labels do not recover raw fusion on arbitrary feasible domains.

**Corollary 3 (strict intervention-width hierarchy).** For every k>=1,
there are models agreeing on all formulas in which each antecedent mentions
at most k distinct writable features, despite arbitrary consequent nesting,
but disagreeing on one (k+1)-feature conjunction conditional.

**Proof.** Use H={{1,...,k+1}}. Every exact branch of an antecedent mentioning
at most k features fixes all h_C in both models, so its endpoint relations
coincide under the same bijection. Induction handles arbitrary nesting.
The conjunction of all k+1 positive features distinguishes as above. QED.

The atomic non-definability is stronger than a bound on experiment depth:
unbounded sequential experimentation on single-feature interventions still
does not identify these simultaneous effects. The width hierarchy is
about the syntax of one intervention, not the total number of feature
names or conditional steps in a formula.

### What full products restore

On a full product, E_(S union T)=E_S composed E_T. For a conjunction t on
J, sequentially execute the resets R_p union R_NOT-p for p in J, then test
t. This relational program has exactly R_t as its endpoint relation.
The equality can fail on feasible subsets: in Theorem 1 every atomic
reset fixes the h_C, while a fused support may release an entire block.
Thus the obstruction is a loss of the support-union composition identity,
not merely coarse observations or classical equivalence of antecedents.

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
preserves every nested formula over P.

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

This is a feature-quotient lower bound, distinct from Corollary 3's
read-only-decision hierarchy. Its supports need not all be disjoint:
S_q and S_p_1 share x_1. Theorem 1's disjointness claim concerns that
theorem's writable features, not this separate optimal-bound example.

## 4. Classifier outputs must be observations, not extra assignments

Suppose the feature criterion holds and a given deterministic raw classifier
is observed through decision atoms D. There exists a feature-only classifier
f:{0,1}^P -> {0,1}^D such that d(w)=f(h(w)) exactly when

    h(w)=h(v) implies d(w)=d(v).                                (4)

This is the familiar functional dependence P -> D. Surjectivity makes f
total and unique. If (4) holds, (3) and induction preserve all nested
formulas whose antecedents use P and whose consequents may observe D, with
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

These are representation and non-identifiability statements for a specified
intervention semantics. They do not infer causal effects from observational
data, classify decidability of every feasible-domain language, or settle
Briggs's general import-export question.

## 5. Precise relation to prior work

The theorem isolates a raw-fusion realization and non-identifiability result;
none of the following broader ideas is claimed as new.

- **Functional dependence and high-order failure.** The maximal frame tests
  and (4) are functional dependencies. Kontinen, Link and Vaananen,
  *Independence in Database Relations* (WoLLIC 2013), proof of Theorem 1,
  pp.186-187, already use a Boolean parity relation with full proper
  projections and a failing higher-order independence claim. Our width
  result is not a discovery of high-order dependence: its extra content is
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
- **Causal abstraction.** Beckers and Halpern (2019), Definitions 3.12-3.17,
  compare intervention cylinders under abstraction; Example 3.16 already
  warns that overlapping macro-observables can constrain which simultaneous
  interventions make sense. Geiger et al. (2025), Definition 25, explicitly
  compare images of solution sets under interventions. Equation (3) is a
  specialized exact-abstraction requirement, not a new general one.
  [Beckers-Halpern text](https://www.cs.cornell.edu/home/halpern/papers/abstraction.pdf),
  [Geiger et al. text](https://www.jmlr.org/papers/volume26/23-0058/23-0058.pdf).
- **Constrained causal models.** Beckers, Halpern and Hitchcock, *Causal
  Models with Constraints* (2023), Sections 3-4, already allow feasibility
  constraints and disconnection of structural equations; their Theorem 2
  gives an axiomatization. Section 2 permits equationless endogenous
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
  arbitrary minimal decision-changing coalitions. Corollary 2 does not
  contradict DL-PPA's instrumented translation into DL-PA (2019, Section
  3, Propositions 6-8), which introduces copied variables and write flags.
  [DL-PPA](https://www.ijcai.org/proceedings/2019/0774.pdf),
  [2021 text](https://arxiv.org/pdf/2104.14884).

The source comparison does not establish publication priority for the
combined theorem. Its defensible mathematical contribution is the explicit
realization/non-identifiability result and the feasible-domain quotient
criterion, rather than another renamed assignment calculus.

## Verification

Run `python models/check_feasible_fusion.py`. It independently enumerates
coordinate endpoints, tests the maximal criterion on small feasible models,
checks minimal supports and all coalition/bit-pattern endpoints in the
realization construction, compares guarded atomic reducts, and exercises
nested formulas and a nonconstant read-only classifier. Finite checks
support the general proofs; they neither prove priority nor replace them.
