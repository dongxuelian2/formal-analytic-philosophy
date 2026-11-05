# Source audit and a defensible main theorem

This audit concerns the raw-variation results in this repository, not the
priority of an entire research program. The claims below distinguish proved
statements, inherited machinery, and publication novelty that remains
unestablished. No search can certify novelty merely by failing to locate a
matching theorem.

## Closest precedents checked

**Briggs (2012).** Sections 1.3 and 3.2–4, especially pp.145 and 154–156,
already give compatible partial-value truthmakers, inclusive fusion,
exact-equivalence replacement, nested consequents, and CM9. The Boolean
overwrite semantics here is the equation-free, all-exogenous specialization:
for M_w=(P,empty,w), intervention u gives M_w[u]=M_(w[u]). Matching verifier
recursions and induction preserve the entire language. This specialization
is our deduction from the definitions, not a separately named theorem in
the source. General causal-model completeness does not automatically prove
completeness for the subclass. [Primary text](https://humanities-web.s3.us-east-2.amazonaws.com/philosophy/prod/2024-08/Briggs%20Interventionist%20Counterfactuals%202012.pdf).

**DL-PPA (2019).** Section 2.2 and Figure 1 retain written-variable
footprints, reject conflicting parallel writes, and give inclusive choice
its left/right/parallel alternatives. Exact NNF antecedents translate
linearly to constant assignments, compatible parallel, and inclusive
choice, and the reverse map is linear. This is a definitional counterpart
of that fragment, not a new program mechanism. The independent PSPACE
algorithm in this repository does not depend on the paper's translation
into DL-PA. [Primary text](https://www.ijcai.org/proceedings/2019/0774.pdf).

**DL-PA complexity.** The QBF encoding by alternating modalities over
positive/negative assignment choice is already in Herzig–Lorini–Moisan–Troquard
(2011), Section 2.3, p.229. The original upper-bound proof was inadequate;
Balbiani–Herzig–Schwarzentruber–Troquard (2014) supply the correction and
reject the intervening EXPTIME claim. The p OR q-only result here is a
restricted-fragment refinement of that established encoding, not new
generic PSPACE behavior. No exact prior publication of that restriction was
verified. [2011 author PDF](https://www.inf.unibz.it/~ntroquard/PAPERS/HeLoMoTr11ijcai.pdf),
[checked author mirror](https://troquard.bitbucket.io/PAPERS/HeLoMoTr11ijcai.pdf),
[2014 correction](https://arxiv.org/pdf/1411.7825).

**Ceteris-paribus logic.** Grossi–Lorini–Schwarzentruber (2013), Section 2,
uses agreement on named propositions; Section 3.1, Theorem 2, encodes
bounded STIT action alternatives with Boolean variables. The general
contrast between unbounded alternatives and explicit Boolean coding is
therefore established. On the full Boolean cube a deterministic update u
also has the immediate expression

    [u]phi = [P minus dom(u)]_CP (L_u implies phi),

where L_u specifies its assigned bits. Expansion over all exact assignments
can be exponential, so this observation alone is not a polynomial
complexity reduction. PECP's arbitrary-model complexity is not the
complexity of our fixed-cube semantics. [Primary text](https://arxiv.org/pdf/1310.6416).

## What the existing proofs actually contribute

- The finite cyclic-group cover addresses arbitrary overlapping raw reset
  supports. Together with the established finite S5^3 undecidability theorem,
  it gives the raw-language finite-validity transfer. Merely exhibiting
  independent supports as a subclass would not suffice.
- The literal-marker lift replaces reset antecedents with pairs of literal
  boxes, retaining non-r.e. finite validity with three nonconstant,
  realizable, genuinely singleton-supported markers. Unrestricted data
  predicates remain essential to the stated result.
- The positive-pair hardness proof restricts an existing Boolean-choice
  mechanism. Its exact restriction is useful, but the broad assignment
  semantics, reduction principles, and complexity phenomenon are inherited.
- The intrinsic finite representation, colored-completion, and rectangular
  import results remain proved repository claims. This focused audit does
  not independently certify their novelty or reopen every proof.

## The product quotient and its constrained-domain limit

The [visible Boolean quotient theorem](visible-boolean-quotient.md) is a
more precise central characterization than “complete values are the sharp
boundary.” In a finite nonempty full-product raw model, the visible truth
map preserves every exact-antecedent endpoint set precisely when each
positive/negative atomic intervention is available and each atomic reset
preserves the other visible bits. It is then onto the Boolean cube and
preserves all nested formulas. Full product is essential; the note supplies
a finite counterexample without it.

This extends the positive case to coarse predicates with arbitrarily large
hidden domains when the visible language cannot observe their residual
freedom. Complete coordinate values are sufficient, not necessary. Adding
hidden-sensitive data predicates can destroy the criterion and restores the
scope of the negative result. The two results are compatible, rather than
a dichotomy covering all possible raw model classes.

The general quotient/preservation method is standard. The raw-model atomic
criterion and its lifting proof are presented as a proved characterization
whose publication novelty remains open. A reasonable project description
is: **raw-variation transfer and visible-quotient theorems connecting finite
product-modal obstruction with existing assignment semantics.**

The [feasible-domain fusion theorem](feasible-fusion-boundary.md) is now
the focused main result. The hidden equality-block/XOR mechanism has a
specific classical precursor: Benaloh–Leichter, *Generalized Secret Sharing
and Monotone Functions*, Theorem 2, applied to the complementary access
structure. Arbitrary coalition realization alone is therefore not a new
contribution. DL-PPA Section 2.2 already shows that endpoint relations lose
information needed by parallel composition; its Propositions 7–8 give the
instrumented translation into DL-PA. These inherited mechanisms are
explicitly separated from the intervention-specific claims.

The strengthened note proves a masked raw realization with an
atomic-isomorphic **full-product** comparison model; sharp world,
coordinate and support-size bounds in the stated equality/disjoint-support
class; parity rigidity at minimum world count; and distinct thresholds for
first distinguishing width and complete endpoint reconstruction. Its
language admits unbounded nesting and relational program composition, with
fusion restricted to explicitly bounded-width primitives. The feature
quotient theorem, by contrast, concerns the base nested conditional language:
quotient-image equality alone does not preserve program intersection.

Precise source comparisons in that note cover generalized secret sharing,
constrained causal models, Beckers–Halpern abstraction, database Armstrong
relations, and read-only classifier logic. Their cited statements do not
directly supply the full masked equal-reduct and size/width package, but
this bounded comparison does not establish publication priority. General
constrained-domain axiomatization and Briggs's causal import–export problem
remain separate and open here.
