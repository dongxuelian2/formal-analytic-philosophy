# Variation semantics: centering audit and an import theorem

## Status and scope

This note establishes a two-point correction to the **14 March 2022 version**
of Hudetz–Crawford, then studies a precisely specified, uncentered local-support
variant. It proves a transition representation and unrestricted **one-way
import** in that variant, with a sufficient condition for two-way import–export.
It also characterizes finite product frames by validity of import, making the
independence assumption an exact boundary rather than an unexamined convenience.
It does not solve Briggs' extended interventionist semantics or claim a new
complete axiomatization. Priority of the import result remains to be established.

## 1. A minimal countermodel to the printed SDA proposition

Hudetz–Crawford [HC], Definition 6(3), requires a true antecedent's variants to
agree with the evaluation point on the verifier's basis; clause (2) already
requires agreement outside it. Consequently, a true antecedent selects only the
original point. Their Proposition 1 states unrestricted SDA. These conflict.

Take one independent Boolean coordinate X, worlds 0 and 1, and atom p meaning
X=1, relevant to X. At 0, the selected sets are

    f(0, ¬p ∨ p) = {0},       f(0, p) = {1}.

Thus `(¬p ∨ p) > ¬p` is true, whereas `p > ¬p` is false. This uses the printed
definitions without any extra assumption. Two worlds are minimal: in a
one-world model success makes every false antecedent selection empty, while
every true antecedent selects that world, so SDA cannot fail.

The surrounding text after Definition 6 explicitly confirms the singleton
consequence; this is not merely an interpretation of an isolated clause.
Definition 8 quantifies over all evaluation points, without restricting the
antecedent to be false. Restricting SDA to points where its disjunctive antecedent
is false avoids this witness, but is a different rule. Berz [B], section 7,
suggests the variation framework as a candidate; its exact version therefore
matters.

### Known general obstruction, not a novelty claim

Strong centering plus SDA collapse results predate this note: see Cariani and
Goldstein [CG], section 4.2. Here is the selection-function form that isolates
the obstruction without assuming antecedent extensionality.

**Proposition.** Let classical normal formulas be interpreted at worlds. Suppose
conditionals use universal quantification over `f(w,A)`, with success
`f(w,A) ⊆ [[A]]`, strong centering `f(w,A)={w}` when `w ⊨ A`, and the formula
scheme SDA. Then `f(w,A)=∅` whenever `w ⊭ A`. Hence every conditional has the
truth conditions of material implication.

**Proof.** At such a point, `A∨¬A` is true. Strong centering makes
`(A∨¬A)>¬A` true. SDA gives `A>¬A`; thus `f(w,A)⊆[[¬A]]`.
Success gives `f(w,A)⊆[[A]]`, so it is empty. Strong centering handles true
antecedents. No arbitrary-consequent definability assumption is needed. □

This is a collapse, not inconsistency. Inconsistency with the package arises
only after adding nonempty selection for at least one attainable false
antecedent. It does not require SEA. Separately, the familiar SEA+SDA⇒AS
obstruction is already recorded in this repository and in [B].

## 2. Exact local-support semantics without strong centering

Fix finitely many independent coordinates I with nonempty finite domains D_i
and the full product Ω=∏D_i. Each atom p has a fixed support S_p⊆I and a
truth set P_p⊆Ω **local to S_p**: points agreeing on S_p agree on p.
Normal formulas use ¬, ∧, ∨. Conditional antecedents must be normal;
consequents may contain conditionals, with classical Boolean connectives.

For families of coordinate sets, write U⊗V={s∪t:s∈U,t∈V}.
At each v define positive and negative verifier families T_A(v), F_A(v):

* Atomic p: T_p(v)={S_p}, F_p(v)=∅ if v∈P_p; reverse them otherwise.
* Negation exchanges T and F.
* Conjunction: T_(A∧B)=T_A⊗T_B;
  F_(A∧B)=F_A∪F_B∪(F_A⊗F_B).
* Disjunction: T_(A∨B)=T_A∪T_B∪(T_A⊗T_B);
  F_(A∨B)=F_A⊗F_B.

The fusion branch in disjunction is retained. Omitting it would be a different
semantics. Define

    R_A(w) = {v : some S∈T_A(v) has v_i=w_i for every i∉S}.
    w ⊨ A>C iff R_A(w)⊆[[C]].

This removes the strong-centering test, retaining weak centering. On the stated
independent-coordinate fragment it is the raw verifier-based construction
suggested by [HC], not an unrelated new semantics.

**Scope warnings.** Locality is an explicit additional hypothesis: [HC]'s
formal definition of models does not impose it on Rel and Prop. We also assume
a full finite product. Single-coordinate closure alone does not imply an
infinite full product (finite-support binary sequences are a counterexample).
Dependent outputs can be predicates on input coordinates; this keeps the
algorithm fixed rather than surgically changing its equations.

**Lemma (support locality).** If S∈T_A(v) and u agrees with v on S, then
S∈T_A(u). The analogous statement holds for F.

**Proof.** Simultaneous structural induction. Atomic locality gives the base
case; negation exchanges the claims. Every fusion support is a union, so
agreement on it gives agreement on both component supports. The union branches
are immediate. The same induction shows T_A(v) is nonempty exactly when A is
classically true at v. □

## 3. Transition representation and import

A partial assignment t is an assignment on a support S. Let E_A consist of
all pairs (S,v restricted to S) for S∈T_A(v), identifying duplicate pairs.
Write w[t] for overwriting coordinates in dom(t) with t's values. Locality makes
membership in E_A independent of the chosen extension v.

**Theorem 1 (overwrite representation).**

    R_A(w) = {w[t] : t∈E_A}.

Moreover, E_(A∧B) is exactly the set of unions t∪s of compatible partial
assignments t∈E_A and s∈E_B. Here compatible means they agree on overlapping
coordinates.

**Proof.** If v∈R_A(w), choose its witness S and t=v restricted to S; agreement
outside S gives v=w[t]. Conversely, if t∈E_A, choose a witnessing extension v.
Then w[t] agrees with v on dom(t), so the locality lemma transfers the verifier
and yields w[t]∈R_A(w). For the conjunction statement, a common world's two
verifiers restrict to compatible assignments. Conversely, any compatible pair
extends to a product point. Locality transfers both verifiers there; their
union verifies the conjunction. □

**Theorem 2 (unrestricted import).** For all normal A,B and all consequents C,
including right-nested conditionals,

    A>(B>C) ⊨ (A∧B)>C.

**Proof.** It suffices to show
`R_(A∧B)(w)⊆⋃{R_B(u):u∈R_A(w)}`. A jointly selected endpoint is
w[t∪s] for compatible t∈E_A,s∈E_B. Compatibility gives
w[t∪s]=w[t][s], a sequentially selected endpoint. This proves the inclusion;
universal quantification over the larger sequential set entails truth over the
joint set. No restriction on C is used. □

**Theorem 3 (a safe two-way criterion).** If every t∈E_A and s∈E_B are
compatible, the two endpoint sets are equal, so both import and export hold
for this pair of antecedents at every point. In particular, this holds when
the unions of supports of atoms occurring in A and B are disjoint.

**Proof.** Every sequential endpoint has form w[t][s]. Under compatibility it
equals w[t∪s], which is jointly selected by Theorem 1. The reverse inclusion
is Theorem 2. Formula verifier supports lie in the union of their atomic
supports, so disjoint total supports imply compatibility. □

The criterion is sufficient, not necessary. For instance, on one Boolean
coordinate A=(p∨¬p), B=p has conflicting verifier pairs, but both the joint and
sequential endpoint sets are {1} at every point.

### Export fails even with a satisfiable conjunction

Let Ω={0,1}², p mean x=1 with support {x}, q mean y=1 with support {y}.
At w=(0,0), take A=p, B=(¬p∨q), C=p. Then

    R_(A∧B)(w) = {(1,1)},
    ⋃{R_B(u):u∈R_A(w)} = {(0,0),(0,1),(1,1)}.

Thus `(A∧B)>C` is true but `A>(B>C)` false. Both antecedents and their
conjunction are satisfiable; this is not an empty-conjunction artefact.
Consequently an undirected “IE is valid” assertion would conceal a real
asymmetry. These results concern the explicitly defined raw-variation class,
not Briggs' modified-model semantics.

## 4. A sharp finite-frame representation boundary

Retain finitely many coordinates, but now allow any nonempty set of feasible
points Ω⊆∏D_i. Take D_i to be the projection of Ω on coordinate i, so unused
coordinate values are excluded. Keep local atoms and the raw verifier rule;
require that every coordinate equality `x_i=d` is available with support {i}.
Conjunctions of these atoms and a contradictory consequent are therefore
expressible. Selections and truthmaker extensions range only over Ω. The
theoretical result in this section also permits infinite coordinate domains:
only the number of coordinates must be finite, and the language must contain
the required equality predicates. Finite domains are used by the executable
checker, not by this proof. Empty selections use ordinary vacuous truth.

**Theorem 4 (import characterizes rectangularity).** The following are equivalent:

1. Import is valid for all normal antecedents and all consequents on this model.
2. Import holds for the special instances with A one coordinate equality,
   B a complete specification of the other coordinates, and consequent ⊥.
3. Ω is the full product of its coordinate projections.

**Proof.** (3)⇒(1) is Theorem 2; (1)⇒(2) is immediate.
For (2)⇒(3), first suppose there are at least two coordinates. Fix w,v∈Ω
and i. If the point u obtained from w by replacing just coordinate i with v_i
were absent, take A=(x_i=v_i) and B=∧_{j≠i}(x_j=v_j). Then R_A(w)=∅,
so A>(B>⊥) is true. But v∈R_(A∧B)(w): its joint verifier covers every
coordinate. Thus (A∧B)>⊥ is false, contradicting (2). Every single-coordinate
splice therefore exists. Given any tuple of projected coordinate values,
start from any point and replace coordinates one at a time. Finiteness gives
a point with exactly the desired tuple. For zero or one coordinate,
rectangularity follows directly from nonemptiness and the definition of the
projections. □

**Nonvacuous strengthening.** The same rectangularity boundary holds if import
is tested only at points where both stages of sequential evaluation are
nonempty. For a missing splice u=w[i←v_i], take instead

    A = ((x_i=w_i) ∨ (x_i=v_i)),
    B = ∧_{j≠i} ((x_j=w_j) ∨ (x_j=v_j)),
    C = (x_i=w_i).

Every verifier of A has support {i}; its only two possible outcomes are w and
the absent u. Thus R_A(w)={w}. Every verifier of B has support I\{i}, and B
is true at w, so R_B(w) is nonempty and every member satisfies C. The nested
conditional is therefore true with both stages nonempty. The conjunction's
verifier has support I, and v satisfies A∧B, so v is a joint outcome. Since
v_i≠w_i, C fails there. This is an import failure with **both antecedents true
at the original point**, not an artefact of vacuous truth. No nontrivial-change
requirement is imposed: the first stage is intentionally an identity update.

This is an exact representation of the feasible state-space boundary, not a
complete representation of arbitrary abstract conditional algebras. The result
does not assume SEA or a similarity ordering. It shows why correlations or
integrity constraints between declared independent features can invalidate
import: an intermediate input needed by sequential reasoning may not exist.
For Ω={(0,0),(1,1)}, w=(0,0), A=(x=1), B=(y=1), the nested conditional
A>(B>⊥) is vacuously true but the joint conditional is false.

Atomic locality is independently essential. Even on the full Boolean square,
an atom A that holds only at (1,1) but is incorrectly assigned support {x},
together with B=(y=1), gives that same failure at (0,0). Such an A violates
our model assumption and explains why it cannot be silently omitted.

The finite-coordinate condition is sharp for this characterization as stated:
finite-support binary sequences are closed under every finite coordinate splice
but not an infinite full product. With only finitely supported atomic formulas,
the import proof still works there. Thus finite-coordinate syntax cannot enforce
availability of arbitrary infinite joint assignments.

## 5. Target rules and a finite check

**SDA and MP hold throughout the class.** Every A-verifier remains an
A∨B-verifier, giving `R_A(w)∪R_B(w)⊆R_(A∨B)(w)` and hence SDA.
If A is true at w, any verifier at w shows w∈R_A(w); hence MP holds even for
nested consequents. Equality in the SDA inclusion is not asserted: fused
verifiers may add jointly changed endpoints.

**AS and classical-equivalence replacement fail.** On the same Boolean square,
let r mean x≠y, relevant to both coordinates. At (0,0), p>r is true, but
(p∧q)>r and (p∨(p∧q))>r are false. The latter antecedent is classically
equivalent to p. This refutes theorem-level RCEA, not merely the stronger
local rule with a premise A↔B evaluated only at the current point.

**CC fails.** At (1,0), both p∨¬p and r are true. Nevertheless
(p∨¬p)>r is false because the variant (0,0) falsifies r.

Nonvalidity here means existence of these countermodels, not that every
model must fail each rule. No global impossibility of the target SDA/MP/non-AS/
non-CC/non-SEA package follows: the class above meets that logical profile.

Run `python models/check_variation.py`. It implements the full positive and
negative support recursion, reproduces the centered countermodel and all
nonvalidities above, and checks 24,336 ordered formula/world cases on the
Boolean square, including 800 disjoint-support cases. The finite computation
also checks all 255 nonempty subsets of the Boolean 3-cube: the special import
instances identify exactly its 27 rectangular subframes. The computation
also validates 2,304 nonvacuous missing-splice witnesses with both stages
nonempty. It
does not prove the theorems; the proofs above do. No SAT/SMT or proof assistant
verification is claimed. Finite evaluation is effective by enumerating points
and verifier supports; no favorable worst-case complexity bound is claimed.

## 6. Remaining central problem

The next target is an intrinsic representation or complete axiomatization of
the transition families generated by local exact verifiers. The overwrite
normal form is a proved structural lemma, not that complete characterization.
A second target is a necessary-and-sufficient syntactic condition for export
that is less expensive than enumerating the endpoint relations. Briggs' IE
question must be treated separately from this raw-variation semantics.

## References actually used

* [HC] Laurenz Hudetz and Neil Crawford (14 March 2022), *Variation semantics:
  when counterfactuals in explanations of algorithmic decisions are true*,
  Definitions 1–8 and Proposition 1, especially pp. 19–20 and 26–27.
  https://philsci-archive.pitt.edu/20626/1/Counterfactuals%202022-03-14.pdf
* [B] Cordelia Berz (2026), *Exploring the Logic of Counterfactuals for
  Explaining Algorithmic Decisions*, sections 5–7.
  https://doi.org/10.1007/s11245-026-10441-2
* [CG] Fabrizio Cariani and Simon Goldstein (2020; online 2018), *Conditional
  Heresies*, *Philosophy and Phenomenological Research* 101(2), 251–282,
  section 4.2. https://doi.org/10.1111/phpr.12565
* Rachael Briggs (2012), *Interventionist counterfactuals*, *Philosophical
  Studies* 160, 139–166. https://doi.org/10.1007/s11098-012-9908-5
  The [full text](https://humanities-web.s3.us-east-2.amazonaws.com/philosophy/prod/2024-08/Briggs%20Interventionist%20Counterfactuals%202012.pdf)
  has now been checked: Sections 3.2–4 give exact truthmakers and the
  sound/complete causal-model calculus. The later
  [source audit](novelty-audit.md) identifies the Boolean overwrite case as
  its equation-free specialization. The unrestricted causal-model
  import–export question is not settled by the raw results here.

