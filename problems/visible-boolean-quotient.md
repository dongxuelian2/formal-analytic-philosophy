# When raw interventions have a faithful Boolean quotient

Complete Boolean coordinate values are sufficient for assignment semantics,
but are not necessary. This note characterizes exactly when a finite local
raw model, possibly containing hidden values and overlapping supports, has
the same observable intervention outcomes as the Boolean cube.

The characterization is relative to a specified visible vocabulary. It is
not a classification of every decidable raw-variation fragment, and its
priority has not been established. The modal preservation argument is the
standard bounded-morphism argument; the point requiring proof is that the
atomic conditions lift through raw support fusion.

## 1. Setting and criterion

Let W be a nonempty finite full product of nonempty coordinate domains.
Fix a finite set P of visible atoms. Each p has a support S_p and a truth
set local to S_p, with the raw exact-verifier semantics from the
[variation note](variation-centering-and-import.md). All formulas below use
only P. Antecedents are free normal Boolean syntax; consequents may nest
conditionals. Define

    h(w)(p) = 1 iff w satisfies p,
    E_p = R_p union R_NOT-p = agreement outside S_p.

The two conditions use only visible truth sets and atomic endpoint relations:

1. **Literal availability:** for every w and p, both R_p(w) and
   R_NOT-p(w) are nonempty.
2. **Visible noninterference:** if w E_p v and q differs from p, then
   h(w)(q)=h(v)(q).

Let Q_P be the full Boolean cube on P, with its usual constant assignments.
For normal A let U_A be its exact partial-assignment verifiers: normalize
negations exactly, interpret a literal as its one-feature assignment,
conjunction as compatible union, and disjunction as either branch or a
compatible union of both. Thus

    R_A^Q(x) = {x[u] : u in U_A}.

This is the existing assignment semantics, not the set of all assignments
that merely make A classically true.

**Theorem 1 (atomic criterion for the visible Boolean quotient).** Under
the stated raw-model hypotheses, the following are equivalent:

(i) Literal availability and visible noninterference hold.

(ii) For every normal A and every w,

    h[R_A(w)] = R_A^Q(h(w)).                         (1)

(iii) Equation (1) holds for each literal antecedent.

When these conditions hold, h is onto Q_P, and for every state formula phi
over P, including arbitrarily nested consequents,

    W,w satisfies phi iff Q_P,h(w) satisfies phi.    (2)

The theorem preserves endpoint sets after projection. It does not identify
individual raw successors, multiplicities, coordinate supports, or hidden
states with Boolean assignments.

## 2. Proof

For S a coordinate set, write E_S for agreement outside S. Full products
satisfy

    E_(S_1 union ... union S_k) = E_S_1 composed ... composed E_S_k.

Indeed, every coordinate in the union can be changed to its target value
at one of the steps whose support contains it, while all other coordinates
retain their current values. Every intermediate tuple is in W. The reverse
inclusion is immediate. Consequently, a predicate invariant under each
E_S_i is invariant under E_(union S_i). This is the full-product step.

Assume (i). A nonempty consistent conjunction t of literals specifies a
partial visible assignment u with domain J. Its raw endpoints are exactly

    {v : w E_(union_{p in J} S_p) v and h(v) extends u}.       (3)

This follows directly from the exact-verifier rule for conjunctions of
literals. Repetitions do not change the union support. An inconsistent
conjunction has no endpoints, since a common verifying world cannot satisfy
opposite literals.

For the forward inclusion in (1) for t, an endpoint in (3) has the required
bits on J. For q outside J, noninterference makes q invariant under every
E_p, p in J, and hence under their union-support relation by the preceding
product identity. Its q bit therefore equals that of w. The projected
endpoint is precisely h(w)[u].

For the reverse inclusion, order the distinct p in J and perform their
specified literal interventions successively. Availability supplies a next
world at each step. Noninterference preserves every earlier assigned bit
and all visible bits outside J. The resulting v agrees with w outside the
union of these supports and satisfies all literals of t, so belongs to (3).
Thus its image is h(w)[u]. This argument realizes simultaneous raw
verification; it does not assume a law equating arbitrary sequential and
simultaneous raw interventions.

For general A, exact double-negation and De Morgan normalization and
contextual inclusive splitting give a finite family of literal-conjunction
branches. Equivalently, an induction on verifier derivations gives those
branches, retaining left, right, and fusion alternatives at disjunctions.
Raw R_A is their endpoint union; U_A is the family of their consistent
visible assignments. Applying the conjunction result branch by branch
proves (1). An exponentially large branch family is harmless for this
semantic proof; it is not an efficient compilation claim.

Starting from any world, set each atom in P to an arbitrarily prescribed
bit by the same sequential construction. This proves that h is onto; for
empty P the assertion follows from W being nonempty.

For (2), use induction on state formulas. Atoms follow from the definition
of h and Boolean cases are immediate. At a conditional, the induction
hypothesis makes its consequent depend only on the visible image, and
(1) equates exactly the raw and Boolean successor images. Universal
quantification over them gives the conditional step.

Finally, (ii) implies (iii). Under (iii), each literal's right side is the
singleton obtained by setting its target bit, so its raw successor set is
nonempty. Every endpoint of R_p or R_NOT-p agrees with the source on every
other visible bit. Their union is E_p, giving noninterference. Hence
(iii) implies (i). QED.

## 3. Consequences and necessary limits

**Hidden values need not be removed.** Let coordinate p have domain
{0,1} times H_p for any nonempty finite H_p, and let visible p read only
the first bit, with support that entire coordinate. The theorem applies
even though an intervention leaves every hidden H_p value free. Additional
coordinates ignored by all visible atoms may also lie in several stipulated
supports, producing overlapping supports. Formula truth over P still
coincides exactly with the Boolean cube.

**Corollary 2.** Across the class satisfying (i), satisfiability and validity
for the visible language coincide with those of Q_P. Thus the existing
PSPACE bounds, deterministic-fragment NP/coNP bounds, and reduction calculus
from the [Boolean note](value-complete-interventions.md) transfer unchanged
when the finite visible vocabulary is input-dependent.

This is a transfer of already established complexity results. It excludes
arbitrary additional data atoms that read hidden values. Such observations
can violate noninterference, which is why this theorem does not conflict
with the three-marker non-r.e. result. It also does not bound the number of
hidden worlds or solve recognition from a succinctly specified raw model.

**Full-product counterexample.** The hypothesis cannot simply be replaced
by an arbitrary feasible subset, even if (i) holds. Take Boolean coordinates
(a,b,c,x,y), retain only the 16 states with x=y, and define

    p=a, support {a,x};
    q=b, support {b,y};
    r=c XOR x, support {c,x,y}.

All atoms are local to their stated supports. A p reset cannot change x,
since y is held fixed and feasibility requires x=y; likewise a q reset
cannot change y. An r reset preserves a,b. Every literal is available
(change a, b, or c as appropriate), and each reset preserves the other
visible bits. Nevertheless the joint support of p AND q permits x and y
to change together. From (0,0,0,0,0), the endpoint (1,1,0,1,1) verifies
p AND q and changes r from 0 to 1. Its image is not the Boolean assignment
outcome, which leaves r=0. Thus even an onto map with correct literal
images need not preserve fused antecedents outside the full-product class.

Dropping availability also fails: a constantly true atom cannot implement
its negative assignment. Dropping noninterference fails already when
p and q read the same Boolean coordinate. These failures concern the
specific quotient property, not decidability in general.

## 4. Position and verification

The target assignment semantics is inherited from Briggs's equation-free
Boolean specialization and DL-PPA's constant-assignment fragment; see the
[source audit](novelty-audit.md). Surjective endpoint preservation and its
induction for modal formulas are standard bounded-morphism ideas. What is
proved here is the lifting of two atomic conditions to all exact-verifier
antecedents in this raw full-product class, with a converse and an explicit
failure on a nonrectangular feasible domain. No priority claim follows from
having supplied this proof.

Run `python models/check_boolean_quotient.py` for independent comparisons
of raw per-world verifier recursion against partial-assignment semantics,
exhaustive small atomic criteria, nested formulas, hidden-value examples,
and the non-product counterexample. These are finite checks of the proof's
claims, not a substitute for the argument or a novelty test.
