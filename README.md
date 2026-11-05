# Formal Analytic Philosophy

Mathematical research in philosophical logic, formal semantics, and mechanized reasoning.

## Current research

### Counterfactual Logic for Explainable AI

**Central problem.** Characterize the strongest coherent and computationally tractable semantics for counterfactual explanations of algorithmic decisions, with particular attention to the inference principles identified by Berz (2026).

We seek a substantial new **representation or completeness theorem** for a class of counterfactual models. If the proposed principles are incompatible, the alternative goal is a sharp **impossibility theorem** with explicit minimal assumptions and countermodels.

The target properties include simplification of disjunctive antecedents (SDA) and appropriate modus ponens (MP), while avoiding unrestricted antecedent strengthening (AS), conjunction conditionalisation (CC), and substitution of equivalent antecedents (SEA). Their exact formulations, scopes, and mutual dependencies must be established before selecting a semantics.

Research entry point and precise agenda: [Counterfactual semantics](problems/counterfactual-semantics.md).

## Results

[Feasible-domain fusion boundary](problems/feasible-fusion-boundary.md):

- Equality-constrained Boolean models with pairwise disjoint, inclusion-minimal writable supports can realize any prescribed antichain of nonsingleton feature coalitions as the minimal interventions capable of changing a read-only decision.
- Guarded models have isomorphic atomic intervention systems, including all decision labels, but different fused interventions. For every k, agreement on all interventions of width at most k does not determine width k+1, even with arbitrary nesting.
- On arbitrary finite feasible domains, literal availability and one maximal-support frame test per feature characterize exactly the faithful Boolean feature quotient. The worst-case witness width of m-1 for m features is optimal.
- Read-only classifier outputs extend the quotient precisely when they factor through the visible features. Generic footprint sensitivity, functional dependence, and causal abstraction are attributed to prior work; novelty of these specific constructions remains unestablished. [Finite checks](models/check_feasible_fusion.py).

[Visible Boolean quotient](problems/visible-boolean-quotient.md):

- On finite full-product raw models, literal availability and preservation of the other visible bits are necessary and sufficient for the visible truth map to preserve every normal-antecedent endpoint set.
- The map is onto the Boolean cube and preserves arbitrary nested consequents. Coarse predicates may retain unbounded hidden values; complete coordinate values are sufficient, not necessary.
- A 16-world feasible-domain counterexample shows why atomic conditions alone do not suffice without the full-product hypothesis. [Independent checks](models/check_boolean_quotient.py) compare raw verifier recursion with visible assignment semantics.
- The [source audit](problems/novelty-audit.md) distinguishes inherited Briggs/DL-PPA semantics, classical complexity machinery, and the raw-model transfers. The quotient method is standard; novelty of the specific characterization remains unestablished.

[Value-complete intervention boundary](problems/value-complete-interventions.md):

- Literal-only coarse-predicate interventions still have non-r.e. finite validity, even with nonconstant, realizable markers of genuinely relevant singleton support. Excluding tautological antecedents does not suffice.
- For explicit complete Boolean feature values, full Boolean antecedents and nested consequents have PSPACE-complete satisfiability/validity and a sound, weakly complete intervention-reduction calculus.
- PSPACE hardness already uses only non-tautological positive alternatives p OR q; deterministic literal-conjunction assignments instead give NP/coNP satisfiability/validity for tree formulas.
- The positive semantics is an equation-free Boolean specialization of Briggs and a definitional counterpart of a DL-PPA fragment. [Checks](models/check_interventions.py) cover reduction, overwrite, literal projection, and guarded QBF translations. The two model classes form a proved contrast, not a classification of all decidable restrictions.

[Finite axiomatization boundary](problems/finite-axiomatization-boundary.md):

- Finite-valid formulas of the full raw-variation language are not recursively enumerable, already in a fragment with three fixed tautological antecedents.
- Therefore no effective system with finite proofs is both sound and weakly complete for all finite local product models with unbounded domain sizes.
- A finite cyclic-group cover handles arbitrary overlapping supports and proves exact correspondence with finite S5 product modalities, using the classical finite-product undecidability theorem of Troquard–Walther.
- The one/two-reset fragments retain the classical finite-complete S5/S5×S5 Hilbert calculi. This is not a completeness result for the full conditional language or an impossibility theorem for infinite-model semantics.
- [Cover checker](models/check_modal_cover.py): 792 support/domain patterns and 1,983,006 nested formula/world evaluations.

[Colored completion is NP-complete](problems/colored-completion-complexity.md):

- Matching complexity bounds for finite explicit atomic extension and observed realization.
- Hardness already with two distinct support equivalences, standard uncolored product geometry, and each support type separately representable.
- A direct four-marginal integer criterion for the two-support fork, with a complete polynomial reduction from partial Latin square completion.
- [Reproducible checks](models/check_completion.py): 10,256 small fork inputs and all 11,813 valid partial Latin squares of orders 1–3.
- One support type is polynomial-time decidable. Two support types permit NP-completeness when the number of propositional truth bits grows. Classical marginal, Latin-square, and PR-box precedents are explicitly attributed.

[Intrinsic finite representation](problems/intrinsic-finite-representation.md):

- Necessary and sufficient conditions for abstract conditional systems on a finite world set: atomic reset, truth-local Boolean completion of equivalences, and exact-verifier generation.
- Constructive coordinate recovery and uniqueness of the full conditional extension from positive/negative atomic data.
- A joint-color obstruction, complete single-support test, and NP upper bound for finite explicit observed realization.
- [Finite representation checker](models/check_intrinsic.py): 57,600 atomic inputs and 84,672 bounded-depth formula matrices, independently compared with coordinate representations.

The factor-equivalence geometry and related independence/assignment frameworks are attributed to prior work. The combined theorem's priority remains unestablished; this is not a finite equational axiomatization or an infinite-model theorem.

[Variation centering audit and import boundary](problems/variation-centering-and-import.md):

- A minimal two-point countermodel to unrestricted SDA in the 14 March 2022 centered variation definition.
- An exact-overwrite representation, one-way import theorem, and sufficient two-way criterion for explicitly defined uncentered local-support semantics.
- A sharp finite-frame characterization: with coordinate equality atoms, import is valid exactly on Cartesian products of coordinate projections.
- Explicit AS, SEA, CC, and export countermodels; [standard-library finite checks](models/check_variation.py).

These are proved intermediate results, not a completed axiomatization or a verified priority claim. Briggs' extended-semantics IE question remains separate and open here.

## References

- Cordelia Berz (2026), *Exploring the Logic of Counterfactuals for Explaining Algorithmic Decisions*, *Topoi*. https://doi.org/10.1007/s11245-026-10441-2
- Rachael Briggs (2012), *Interventionist Counterfactuals*, *Philosophical Studies* 160, 139–166. https://doi.org/10.1007/s11098-012-9908-5
- Stanford Encyclopedia of Philosophy, *Counterfactuals*. https://plato.stanford.edu/entries/counterfactuals/

## Working style

See [AGENTS.md](AGENTS.md). The repository is organized around mathematical questions and verified results, not a software platform.


