# Counterfactual semantics for algorithmic explanations

## Target

Find a mathematically precise class of counterfactual models relevant to algorithmic explanations and prove a new general theorem describing its expressive power and inference principles. Prefer a representation, correspondence, axiomatization, or completeness theorem. If the central desiderata are impossible in the intended class, prove the strongest informative impossibility theorem and identify minimal hypotheses.

**Primary source:** Cordelia Berz, *Exploring the Logic of Counterfactuals for Explaining Algorithmic Decisions*, *Topoi* (published 16 October 2026), https://doi.org/10.1007/s11245-026-10441-2.

## Logical starting point

Write `A > C` for the counterfactual conditional "if A were the case, C would be the case." Assess the exact form and domain of the following candidate principles in the cited source:

- **SDA (simplification of disjunctive antecedents):** `(A ∨ B) > C` entails `(A > C) ∧ (B > C)`.
- **MP (modus ponens):** from `A > C` and `A`, infer `C`, under the appropriate restrictions.
- **AS (antecedent strengthening):** from `A > C`, infer `(A ∧ B) > C`; unrestricted validity is unwanted.
- **CC (conjunction conditionalisation):** verify the exact definition used by the source before encoding it.
- **SEA (substitution of equivalent antecedents):** replacing the antecedent with a logically equivalent one; unrestricted validity is unwanted.
- **IE (import–export):** investigate the treatment of nested conditionals in relevant interventionist extensions; first identify the precise statement and known partial results.

A fundamental starting constraint: **SDA + SEA implies AS** over a classical Boolean antecedent language. Given `A > C`, use `A ↔ (A ∨ (A ∧ B))` and SEA to infer `(A ∨ (A ∧ B)) > C`; then SDA gives `(A ∧ B) > C`. Thus, any satisfactory proposal with SDA and failure of unrestricted AS must avoid unrestricted SEA or alter another assumption. This is a baseline observation; novelty must lie elsewhere.

**Important semantic distinction:** saying that AS or SEA is *not valid* means some admissible model refutes the inference; it does not mean every model refutes it.

## Research attack

1. Establish a complete, accurately sourced inventory of the relevant axioms and existing semantic characterizations (Lewis–Stalnaker, strict conditionals, Briggs/interventionist, and subsequent alternatives).
2. Choose a promising semantic family motivated by a concrete logical need; articulate why it is not just a rephrasing of known selection-function, premise, team, or interventionist semantics.
3. For small finite structures, automate satisfaction and countermodel searches to identify independence phenomena and plausible semantic correspondences.
4. Formulate the largest defensible general theorem: representation, exact characterization, decidability/complexity, or sharp impossibility. Give a mathematical proof and, where valuable, machine-checked components.
5. Connect the result back to actual counterfactual explanations: what changes in the inferences an explainer may soundly make?

## Literature to inspect

- Berz (2026): https://doi.org/10.1007/s11245-026-10441-2
- Briggs (2012), *Interventionist Counterfactuals*: https://doi.org/10.1007/s11098-012-9908-5
- Stanford Encyclopedia of Philosophy, *Counterfactuals*: https://plato.stanford.edu/entries/counterfactuals/
- Hudetz and Crawford (2022), as cited by Berz: retrieve the original work and its technical definitions before building on its claims.

## Current status

See [variation centering and import](variation-centering-and-import.md) for the initial correction and frame boundary, and [intrinsic finite representation](intrinsic-finite-representation.md) for an exact same-world representation criterion from abstract conditional relations.

The [colored-completion complexity theorem](colored-completion-complexity.md) settles the finite explicit decision problem as NP-complete, already with two support types and otherwise standard geometry. A four-marginal integer criterion eliminates Boolean-completion quantification in that fork fragment. One support type is tractable; fixed-color forks are also tractable. The [finite axiomatization boundary](finite-axiomatization-boundary.md) now proves that full finite validity is not recursively enumerable: no effective finite-proof calculus can be sound and complete for that unrestricted finite semantic class. An exact three-reset modal fragment already supplies the obstruction, while one/two-reset fragments have classical finite-complete Hilbert systems. Further positive completeness questions must explicitly restrict the language or models, or consider an infinite-model semantic class; priority assessment also remains open. Existing independent-coordinate, factor-equivalence, marginal, and Latin-square results are not claimed as new.
