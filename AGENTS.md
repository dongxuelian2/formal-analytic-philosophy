# Research Instructions

## Objective

Pursue a genuinely new, significant theorem in counterfactual logic for explainable AI. The active target is a representation/completeness result for a well-motivated semantic class, or a sharp general impossibility theorem if the desired inference rules cannot coexist. Work directly on that problem. Intermediate lemmas, models, and algorithms are steps toward the main result, not a reason to stop.

## Method

1. Read the primary literature and prior axiomatizations before claiming novelty. Record only the references that actually affect the mathematical argument.
2. Fix an exact language, model class, truth definition, and scope of each inference rule. Distinguish validity, admissibility, non-validity, and a concrete counterexample.
3. Investigate the mathematical obstruction first. In classical propositional contexts, replacement of equivalent antecedents together with SDA entails antecedent strengthening via `A ≡ A ∨ (A ∧ B)`. This is a basic known obstruction, not itself a novel result. Any proposed non-extensional semantics must address it explicitly.
4. Use small-model enumeration, SAT/SMT solving, and independent code checks to discover countermodels and refine conjectures. Promote finite findings to general theorems only with proof.
5. Use Lean or Isabelle/HOL when formal verification materially strengthens the result. Do not substitute successful tool execution for an explanation of what has been proved.
6. Pursue the central theorem until the relevant research or compute budget is exhausted, changing proof strategies when useful. If blocked, leave a concise description of the precise open subproblem and strongest proven facts.

## Repository organization

Keep mathematical notes and completed proofs close to their topic. Use `problems/` for active problem statements and short research notes; add `proofs/`, `models/`, or `papers/` only when there is actual material for them. Prefer a small, readable set of files.

## Writing

State theorems with exact hypotheses, definitions, and proof status. Attribute existing results accurately. Report experiments with enough information to reproduce them. Keep README results concrete and update them when substantial results are verified.

Write concise mathematical prose. No ceremonial CI, hashes, boilerplate reports, artificial progress metrics, or long defensive narratives. Do not add engineering infrastructure without a direct mathematical need. For publishable work, prefer a short conventional paper and complete argument.

## Pull requests

Commit actual mathematical progress and open a PR for review. A PR can contain a new theorem, a rigorously proved obstruction, or a necessary component of the central result. Keep the description focused on what has been established and what remains open. Never misrepresent a conjecture or computational observation as a proof.
