<div align="center">

# Formal Analytic Philosophy

**Mathematical research in philosophical logic, formal semantics, and mechanized reasoning**

[Current research](#current-research) · [Research results](#research-results) · [References](#references)

</div>

---

## Current research

### Counterfactual logic for explainable AI

We seek a representation or completeness theorem for computationally tractable counterfactual semantics for algorithmic explanations. If the target inference principles are incompatible, the goal is a sharp impossibility theorem with explicit minimal assumptions and countermodels.

The research agenda follows the inference principles studied by Berz (2026):

| Role | Inference principles |
| :--- | :--- |
| Target properties | Simplification of disjunctive antecedents (SDA), appropriate modus ponens (MP) |
| Principles to restrict | Antecedent strengthening (AS), conjunction conditionalisation (CC), substitution of equivalent antecedents (SEA) |

The first step is to determine the exact formulations, scopes, and dependencies of these principles.

**[Read the research agenda →](problems/counterfactual-semantics.md)**

## Research results

### Coalition nonidentifiability

**Current manuscript · Five-page expert note**

> [**Read the paper (PDF)**](papers/coalition-nonidentifiability.pdf) · [LaTeX source](papers/coalition-nonidentifiability.tex) · [Full mathematical notes](problems/feasible-fusion-boundary.md)

The note studies hidden raw states under coarse-feature interventions through an endpoint-only interface. It establishes three results:

1. **Coalition realization.** Masked equality-block models realize any nonsingleton antichain of minimal possible decision-changing coalitions and admit full-product comparisons with isomorphic complete literal-intervention reducts.
2. **Exact lower bounds.** For Boolean equality solution sets with disjoint supports and literal availability, the lower bounds are $2^{n+|H|}$ worlds, $n+\sum_{C\in H}|C|$ coordinates, and $1+\deg_H(i)$ support size. Support minimality and deterministic literals are unnecessary. Parity and overlapping-support examples violate all three bounds outside this class; the minimal-overlap weakening additionally requires exact conjunction projection.
3. **Distinguishing and reconstruction widths.** First distinguishing width is $\min_{C\in H}|C|$; endpoint reconstruction by local reset programs requires width $\max_{C\in H}|C|$.

The note includes a two-feature example, a mixed pair/triple example, and theorem-level comparisons with prior work, including Herzig–Saffidine (2026). The secret-sharing construction and generic footprint obstruction come from prior work; the masking/isomorphism and equality-class counting arguments are elementary.

**Research status:** expert consultation before any standalone paper submission. Independent novelty and significance remain open. The [consultation brief](papers/coalition-consultation.md) contains a draft question for Herzig, Beimel, and Beckers; external consultation is pending. [Finite verification](models/check_feasible_fusion.py) covers the core construction and the two boundary examples.

### Earlier results

The following results document the preceding stages of the research. Each entry links to its mathematical notes and, where applicable, its finite verification script.

| Topic | Main result | Verification |
| :--- | :--- | :--- |
| [Deterministic fusion](problems/deterministic-fusion-representation.md) | Equality normal form, endpoint-count inversion, affine results | |
| [Visible Boolean quotient](problems/visible-boolean-quotient.md) | Exact criterion for endpoint preservation on full-product models | [Checker](models/check_boolean_quotient.py) |
| [Value-complete interventions](problems/value-complete-interventions.md) | Decidability and complexity boundary for Boolean interventions | [Checker](models/check_interventions.py) |
| [Finite axiomatization](problems/finite-axiomatization-boundary.md) | Non-r.e. finite validity with three reset modalities | [Checker](models/check_modal_cover.py) |
| [Colored completion](problems/colored-completion-complexity.md) | NP-completeness with two support types | [Checker](models/check_completion.py) |
| [Intrinsic finite representation](problems/intrinsic-finite-representation.md) | Necessary and sufficient conditions for coordinate representation | [Checker](models/check_intrinsic.py) |
| [Variation centering and import](problems/variation-centering-and-import.md) | Exact import characterization on finite frames with coordinate equality atoms | [Checker](models/check_variation.py) |

<details>
<summary><strong>Detailed results and applicability conditions</strong></summary>

#### Deterministic fusion representation

The equality normal form, endpoint-count inversion, and affine results belong to the preceding revision and serve as background for the expert note. Further classification remains open.

#### Visible Boolean quotient

- On finite full-product raw models, literal availability and preservation of the other visible bits are necessary and sufficient for the visible truth map to preserve every normal-antecedent endpoint set.
- The map is onto the Boolean cube and preserves arbitrary nested consequents. Coarse predicates may retain unbounded hidden values; complete coordinate values suffice but are unnecessary.
- A 16-world feasible-domain counterexample establishes the need for additional conditions beyond the atomic ones on general feasible domains. Independent checks compare raw verifier recursion with visible assignment semantics.
- The [source audit](problems/novelty-audit.md) attributes Briggs/DL-PPA semantics and classical complexity machinery and distinguishes the raw-model transfers. The quotient method is standard; priority of the specific characterization remains open.

#### Value-complete intervention boundary

- Literal-only coarse-predicate interventions have non-r.e. finite validity, even with nonconstant, realizable markers of genuinely relevant singleton support. The obstruction persists with non-tautological antecedents.
- For explicit complete Boolean feature values, full Boolean antecedents and nested consequents have PSPACE-complete satisfiability and validity, with a sound, weakly complete intervention-reduction calculus.
- PSPACE hardness already holds for non-tautological positive alternatives $p\lor q$. Deterministic literal-conjunction assignments give NP/coNP satisfiability/validity for tree formulas.
- The positive semantics is an equation-free Boolean specialization of Briggs and a definitional counterpart of a DL-PPA fragment. Finite checks cover reduction, overwrite, literal projection, and guarded QBF translations. A classification of decidable restrictions remains open.

#### Finite axiomatization boundary

- Finite-valid formulas of the full raw-variation language are non-r.e., already in a fragment with three fixed tautological antecedents.
- Consequently, every effective finite-proof system for all finite local product models with unbounded domain sizes fails soundness or weak completeness.
- A finite cyclic-group cover handles arbitrary overlapping supports and proves exact correspondence with finite S5 product modalities, using the classical finite-product undecidability theorem of Troquard–Walther.
- The one/two-reset fragments retain the classical finite-complete S5 and S5×S5 Hilbert calculi. Completeness for the full conditional language and infinite-model semantics are separate questions.
- Verified: 792 support/domain patterns and 1,983,006 nested formula/world evaluations.

#### Colored completion complexity

- Matching complexity bounds for finite explicit atomic extension and observed realization.
- NP-hardness with two distinct support equivalences, standard uncolored product geometry, and each support type separately representable.
- A direct four-marginal integer criterion for the two-support fork, with a complete polynomial reduction from partial Latin square completion.
- One support type gives polynomial-time decidability; two support types permit NP-completeness when the number of propositional truth bits grows. Classical marginal, Latin-square, and PR-box precedents are attributed.
- Verified: 10,256 small fork inputs and all 11,813 valid partial Latin squares of orders 1–3.

#### Intrinsic finite representation

- Necessary and sufficient conditions for abstract conditional systems on a finite world set: atomic reset, truth-local Boolean completion of equivalences, and exact-verifier generation.
- Constructive coordinate recovery and uniqueness of the full conditional extension from positive/negative atomic data.
- A joint-color obstruction, complete single-support test, and NP upper bound for finite explicit observed realization.
- Verified: 57,600 atomic inputs and 84,672 bounded-depth formula matrices, independently compared with coordinate representations.

The factor-equivalence geometry and related independence/assignment frameworks come from prior work. The theorem concerns finite representation; priority of the combined result, finite equational axiomatization, and infinite-model extensions remain open questions.

#### Variation centering audit and import boundary

- A minimal two-point countermodel to unrestricted SDA in the 14 March 2022 centered variation definition.
- An exact-overwrite representation, one-way import theorem, and sufficient two-way criterion for explicitly defined uncentered local-support semantics.
- A sharp finite-frame characterization: with coordinate equality atoms, import is valid exactly on Cartesian products of coordinate projections.
- Explicit AS, SEA, CC, and export countermodels, with standard-library finite checks.

These are proved intermediate results. A complete axiomatization, priority verification, and Briggs' extended-semantics IE question remain open.

</details>

## Repository guide

| Location | Contents |
| :--- | :--- |
| [`papers/`](papers/) | Manuscript, LaTeX source, and consultation brief |
| [`problems/`](problems/) | Research questions, mathematical arguments, and source audits |
| [`models/`](models/) | Independent finite-model verification scripts |
| [`AGENTS.md`](AGENTS.md) | Research methodology and writing conventions |

## References

- Cordelia Berz (2026). [*Exploring the Logic of Counterfactuals for Explaining Algorithmic Decisions*](https://doi.org/10.1007/s11245-026-10441-2). *Topoi*.
- Rachael Briggs (2012). [*Interventionist Counterfactuals*](https://doi.org/10.1007/s11098-012-9908-5). *Philosophical Studies*, 160, 139–166.
- Stanford Encyclopedia of Philosophy. [*Counterfactuals*](https://plato.stanford.edu/entries/counterfactuals/).
