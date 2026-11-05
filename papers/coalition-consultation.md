# Coalition fusion: expert consultation brief

## Recommendation

Do not submit the present package as a standalone full research paper yet.
The core is correct under its stated assumptions, but the arbitrary-coalition
mechanism is exactly classical replicated-share secret sharing and generic
endpoint/footprint sensitivity is already in DL-PPA. The extra masking,
atomic-reduct isomorphism, equality-class resource count, and width argument
form a useful specialized synthesis, not a demonstrated substantial new
technique. No identical prior theorem was found in the bounded primary-source
review; this does not establish priority or rule out an immediate reformulation.

The [five-page mathematical note](coalition-nonidentifiability.pdf)
([editable LaTeX](coalition-nonidentifiability.tex)) gives the three core
statements and complete proofs, a two-feature example, a pair/triple example,
and precise failure cases for broader size claims. It excludes the previous
complexity results and newer classification expansions.

The best surviving proof step is the restricted lower bound: each minimal
decision-changing coalition requires a distinct essential equality class,
and literal availability requires a separate private class per feature.
The mask then makes all support coordinates essential while preserving a
complete deterministic atomic reset system. The program-language lifting
is routine isomorphism invariance.

Likely objections are the narrow, presentation-dependent optimum; whether
the mask/counting refinement merits a separate result; and the requirement
that decisions depend on hidden raw state rather than only the coarse
feature vector. If d=f(p), exact feature projection and singleton decision
invariance force f constant, ruling out these effects. This is neither
causal identification nor guaranteed recourse.

## Suggested reviewers

1. **Andreas Herzig.** Coauthor of [DL-PPA (2019)](https://www.ijcai.org/proceedings/2019/0774.pdf) and [Herzig–Saffidine (2026)](https://doi.org/10.1007/s10849-026-09468-w). Best first contact for whether identical literal reducts add anything substantial to known footprint semantics and dynamic-logic translations. The 2026 publisher record lists IRIT-CNRS, Toulouse University. His institutional homepage was not available in this check, so no contact address is inferred.
2. **Amos Beimel.** [Ben-Gurion University homepage](https://www.cs.bgu.ac.il/~beimel/) and [publication list](https://www.cs.bgu.ac.il/~beimel/pub.html), including *Secret-Sharing Schemes: A Survey* (2011). Best for whether the equality-incidence count is already a familiar minimal-CNF resource bound and whether the intervention overlay has independent interest.
3. **Sander Beckers.** [UCL profile](https://www.ucl.ac.uk/mathematical-physical-sciences/dr-sander-beckers); coauthor of [Abstracting Causal Models](https://www.cs.cornell.edu/home/halpern/papers/abstraction.pdf) and [Causal Models with Constraints](https://proceedings.mlr.press/v213/beckers23a/beckers23a.pdf). Best for the semantic status and XAI significance of the one-step constrained-model encoding and hidden-state observation interface.

These are proposed consultation targets, not confirmed reviewers. Nobody has been contacted.

## Unsent consultation question

After crediting the Benaloh–Leichter replicated-share construction and
DL-PPA's footprint sensitivity, does the attached result add an independently
useful theorem: Boolean equality-constrained models with disjoint
inclusion-minimal supports and identical complete literal-intervention
reducts, but an arbitrary antichain of minimal joint decision effects,
together with exact sizes restricted to that architecture and distinct
first-distinguishing/reconstruction widths? Is this already an explicit
result or immediate corollary in the literature, and is the remaining
masking-and-counting argument substantial enough for a short note?

## Exact prior-art comparison

- **Ito–Saito–Nishizeki (1987), Proposition 1 and Theorem 1, pp.99–100:** general access structures. The proof shares across complements of maximal unauthorized sets, giving exactly the copied-block incidence pattern after coalition complementation. [Primary text](https://archiv.infsec.ethz.ch/education/as09/secsem/papers/ItSaNi87.pdf).
- **Benaloh–Leichter (1990), Theorem 2, p.32:** monotone formula secret sharing. AND splits the secret additively; OR replicates. Applied to AND_C OR_(i in C) v_i, it is exactly the hidden XOR/equality construction. The theorem does not state the masked literal-reduct isomorphism or additional n private intervention bits. [Primary text](https://www.cs.cornell.edu/courses/cs754/2001fa/bena88.pdf).
- **Herzig–Maris–Vianey (2019), Section 2.2, Proposition 3, Propositions 7–8:** endpoints alone lose parallel-write information; disjoint entire occurring-variable sets permit sequentialization; copied variables/write flags permit instrumented translation. Constrained support fusion is not their compatible merging of local executions. No claim of discovering generic footprint sensitivity is retained. [Primary text](https://www.ijcai.org/proceedings/2019/0774.pdf).
- **Beckers–Halpern (2019), Definitions 3.12–3.14, 3.17, Example 3.16:** intervention and outcome compatibility, partition-based abstraction, and overlapping macro-variable constraints. Exact feature-image equality specializes this established notion. These statements do not identify joint intervention relations from singletons. [Primary text](https://www.cs.cornell.edu/home/halpern/papers/abstraction.pdf).
- **Beckers–Halpern–Hitchcock (2023), Sections 2–3, Theorem 2 on PDF p.10:** constraints, missing equations and disconnection already supply a context-indexed one-step encoding of the raw endpoints. The encoding here is a deduction from the definitions, not a claimed compositional embedding of nested intervention programs. [Primary text](https://proceedings.mlr.press/v213/beckers23a/beckers23a.pdf).
- **Kontinen–Link–Väänänen (2013), proof of Theorem 1, pp.186–187, and Theorem 5, p.192:** parity hides higher-order independence behind complete proper projections; Armstrong relations realize precisely a dependency consequence set. This is the established high-order phenomenon, not the identical primitive-transition statement or the restricted resource count. [Primary text](https://www.mv.helsinki.fi/home/jvaanane/KonLinVaa.pdf).
- **Herzig–Saffidine (2026), Theorem 7, Section 5.3 and Proposition 9:** flagged intervention translations and equivalence across contexts versus across all interventions. Example 6 differs already at a singleton intervention, unlike the equal-singleton-reduct pair here. This is additional related prior work, not a new research direction. [Primary text](https://doi.org/10.1007/s10849-026-09468-w).

## Correctness checks

The general arguments are the proofs in the note. The existing
`models/check_feasible_fusion.py` was rerun, with only two targeted boundary
checks added: 2,592 overlapping-support and 10,368 parity-constrained
source/partial-assignment comparisons. They check minimal supports,
availability, atomic comparison, and all coalition/sign effects.
Finite tests do not establish either the general theorems or novelty.
