# Coarse predicates versus value-complete feature interventions

This note isolates one semantic boundary: **constraining a coarse predicate about a feature** versus **specifying its complete Boolean value**. Banning explicit tautologies is not enough. With unbounded hidden feature values, even nontrivial literal interventions retain the finite-validity obstruction. With explicit, value-complete Boolean features, the full Boolean-antecedent language has an effective sound and complete reduction calculus and PSPACE-complete satisfiability/validity.

These statements concern formula satisfiability and validity, not CBC on an already supplied finite data set. The existing representation, CBC, and unrestricted finite-validity results are retained.

## 1. A literal-only no-go with genuine, realizable predicates

Let q_1,q_2,q_3 be distinct intervention predicates. Restrict every conditional antecedent to one of the six literals q_i or NOT q_i. Allow ordinary Boolean state connectives and arbitrarily nested consequents. Data atoms are distinct from these markers. Models are finite full products with arbitrary finite domain sizes and local atomic truth, as before. We may further require that each q_i has a singleton support, that this coordinate is genuinely relevant, and that both q_i and NOT q_i have realizations.

**Theorem 1.** Finite validity of this literal-only language is not recursively enumerable, even under those additional requirements and with only three coordinate factors. Thus no effective sound and complete finite-proof calculus exists for this class.

**Proof.** At every raw model,

    R_q union R_not-q = E_support(q).

Consequently the state formula

    (q > phi) AND (NOT q > phi)

is precisely the universal support-reset box applied to phi. Translate a three-modal formula recursively by replacing each box_i psi with this conjunction for q_i and the recursively translated psi. There are no tautological antecedents in the resulting syntax. The translation is computable; it can duplicate subformulas exponentially, which is immaterial to the non-enumerability argument. We do not claim a polynomial reduction from this construction.

For raw-to-product truth preservation, replace each pair of literal boxes by its reset relation and use the finite overlapping-support cover from [the axiomatization-boundary note](finite-axiomatization-boundary.md). This works in particular for singleton supports.

For the reverse direction, start with a finite S5^3 product X_1 times X_2 times X_3 and its arbitrary data valuations. Use raw coordinate domains

    D_i = X_i times {0,1}.

Give q_i support {i}, and let it read the final bit of D_i. It is nonconstant, both literal interventions are feasible, and its unique supporting coordinate is genuinely essential: changing that coordinate's bit changes q_i. Pull data valuations back along the projection D_1 times D_2 times D_3 -> X_1 times X_2 times X_3, and give them full support. Each reset on D_i projects exactly to the i-th product modality, preserving all translated formulas by induction. The extra bit never appears in the data valuation.

Thus finite satisfiability and validity are equivalent to the finite S5^3 problems under the computable translation. The finite-specific undecidability theorem [TW12], finite-model enumeration, and the inverse-image argument in the preceding note imply that literal-only finite validity is not recursively enumerable. QED.

The reason is concrete: q_i=1 does not determine the full value of D_i. It still permits any hidden X_i value. The predicate can have genuinely minimal coordinate support and be nontrivial without being a value-complete assignment. Requiring finite supports, forbidding tautological antecedents, or requiring both literal outcomes to be feasible does not remove this residual freedom.

## 2. The positive semantic restriction

Take an explicitly named, finite set P of Boolean **feature atoms**. Its cardinality varies with the input; it is not a fixed constant. A state is a total valuation w:P->{0,1}. All such valuations are possible. Feature p has exactly singleton support {p}, and its truth is its coordinate value. Thus the literal p completely specifies that feature as 1, and NOT p completely specifies it as 0. There are no additional opaque predicates whose truth tables or hidden supports are existentially chosen.

Normal antecedents are still arbitrary free Boolean syntax over P, with negation, conjunction and disjunction. State formulas have ordinary Boolean connectives and A > phi, with arbitrary consequent nesting. Use the same raw exact-verifier semantics, including the inclusive disjunction-fusion branch. No minimal-change or strong-centering clause is added.

The cube is represented implicitly by its named Boolean features, not by an explicitly listed exponential transition table. Only features appearing in the formula matter: projection to them preserves truth, because antecedents update only their own features and all state atoms read them. A formula therefore has a canonical finite state space of at most 2^n valuations, where n is the number of its feature names. This is a semantic restriction to explicit observable feature values, not a claim that arbitrary-support raw models secretly have bounded size.

An explicitly supplied Boolean decision formula or polynomial-size circuit may be used as an output observation. Its truth is computed from the features, not an independently chosen predicate interpretation. The complexity algorithms below can evaluate such circuits directly in polynomial space; the stated proof calculus uses their Boolean-formula definitions.

**Theorem 2.** In this value-complete Boolean class:

1. satisfiability and validity are PSPACE-complete, already with only non-tautological antecedents p OR q for distinct positive feature atoms;
2. the reduction calculus in Section 4 is sound and weakly complete;
3. when antecedents are restricted to nonempty, consistent conjunctions of feature literals, satisfiability is NP-complete and validity is coNP-complete, despite arbitrary consequent nesting.

The familiar assignment-logic complexity and proof principles are prior work. The result here identifies their exact correspondence with this raw exact-verifier restriction, and contrasts it with Theorem 1.

## 3. Exact partial assignments and polynomial-space evaluation

A partial assignment u is a consistent map from some features to {0,1}. Let w[u] overwrite those features and leave the rest unchanged. Two assignments fuse when they agree on their overlapping domains; their fusion is their union.

After pushing normal-form negations to literals using double negation and De Morgan laws, a positive exact verifier of a literal fixes that feature to its indicated bit. A conjunction fuses one compatible verifier from each conjunct. An inclusive disjunction permits a verifier of either disjunct, or a compatible fusion from both. Thus every exact verifier is a consistent partial assignment, and

    w satisfies A > phi iff phi holds at w[u]
    for every exact partial assignment u of A.

This is an overwrite representation, not classical replacement of equivalent antecedents. For example, p and p OR (p AND q) are classically equivalent, but the latter additionally permits the intervention setting both p and q.

**Polynomial-space upper bound.** Do not expand the potentially exponential assignment family or reduction normal form. Generate its derivations depth first: at a disjunction choose left, right, or both; at a conjunction visit both; accumulate a partial bit assignment and reject conflicting writes. Every branch traverses at most the antecedent parse tree, so its description and working storage are polynomial in the input length. Enumerate all such branches, ignoring inconsistent ones, and recursively evaluate the consequent at the overwritten valuation. Duplicate derivations cause no problem.

For arbitrary nesting, keep the current valuation, the current antecedent-generation state, and a stack of formula positions. Each conditional reduces the remaining state-formula nesting depth. The total stack and assignment storage are polynomial, even though runtime can be exponential. Boolean connectives are evaluated depth first as well. Satisfiability additionally enumerates the n initial feature bits; validity checks all of them. Hence both problems are in PSPACE.

**Lower bound.** Translate a closed quantified Boolean formula by leaving its Boolean matrix unchanged and using

    forall p. psi  ->  (p OR NOT p) > translation(psi),
    exists p. psi  ->  NOT ((p OR NOT p) > NOT translation(psi)).

Because p has a value-complete singleton support, the reset has exactly the two possible p values as endpoints, all other features fixed. This translation is linear in QBF syntax and preserves truth by induction. A closed translated QBF has the same truth at every initial valuation: each matrix variable is bound. Therefore its satisfiability and its validity are both equivalent to QBF truth. The standard PSPACE-hardness of QBF establishes both lower bounds.

**Stronger lower bound without tautological interventions.** For each quantified variable x_i, introduce a fresh pair p_i,q_i, initially 0,0. Let G be the conjunction fixing all these initial bits to zero, and let g_i be p_i XOR q_i. Translate matrix x_i as p_i and quantifiers by

    forall x_i. psi -> (p_i OR q_i) > (g_i -> translation(psi)),
    exists x_i. psi -> NOT ((p_i OR q_i) > NOT (g_i AND translation(psi))).

On input 00 the antecedent p_i OR q_i selects the three outcomes 10, 01 and 11: the third is the required fusion outcome. The guard g_i filters that outcome, leaving the two Boolean choices. Every future pair remains 00 because pairs are fresh and each is intervened on once in prefix order. Induction on the QBF prefix therefore proves that G AND the translation is satisfiable exactly when the closed QBF is true, and that G -> the translation is valid exactly when it is true. The translation is linear: each quantified subformula occurs once, and each guard has constant size. Every conditional antecedent is a nonconstant, feasible disjunction of two positive, distinct feature settings. Thus the PSPACE jump is not an artifact of permitting explicit tautological interventions.

**Deterministic fragment.** A consistent conjunction t specifies exactly one partial assignment u_t. Evaluate t > phi simply by evaluating phi at w[u_t]. For a fixed initial valuation, depth-first traversal of the formula tree with an environment stack is polynomial in its length. Guessing the initial bits proves NP membership for satisfiability, and propositional satisfiability is already a sublanguage; validity is its coNP dual. Nested constant assignments do not require exploring choices.

The parameterized cube is implicit; with a fixed number of features, bottom-up computation over its fixed state space is polynomial in formula length. This does not turn the uniform problem above into a polynomial-time one.

Writing (p>phi) AND (NOT p>phi) in this deterministic syntax duplicates phi. Repeated expansion of compact QBF resets may be exponential, so it does not contradict the NP/coNP bound. Formula inputs here are ordinary syntax trees; a DAG with shared subformulas or a separate succinct program-choice operator would be a different input representation.

## 4. A sound and complete reduction calculus

Write [A]phi for A>phi. Use classical propositional tautologies, modus ponens, and replacement of proved **state-formula** equivalents in Boolean and consequent contexts. Do not allow arbitrary replacement of classically equivalent antecedents. Feature names are coordinate parameters: there is no unrestricted substitution rule replacing a feature by an arbitrary formula inside assignment targets.

The following finite collection of axiom schemes and exact antecedent rewrites is effective.

### Exact antecedent normalization

Use double-negation and De Morgan rewrites inside normal antecedents, and associativity/commutativity of conjunction. These preserve positive and negative exact verifiers, not merely classical truth. Once in negation normal form, use the inclusive-splitting schemes

    [A OR B]phi <-> [A]phi AND [B]phi AND [A AND B]phi,

    [D AND (A OR B)]phi <->
       [D AND A]phi AND [D AND B]phi AND [D AND A AND B]phi.

The first scheme is the familiar inclusive-disjunction conditional pattern, also present as Briggs' CM9 [B12]. Its application here is justified by the chosen raw semantics, not by importing Briggs' entire structural-equation calculus.

In each branch the number of disjunctions in that antecedent decreases. Reassociation allows any disjunction in a conjunction context to be exposed. Iteration therefore terminates at conjunctions of literals, although the output can be exponentially larger.

An inconsistent literal conjunction t satisfies

    [t]phi <-> TRUE.

For a consistent literal conjunction t, use the terminal-clause reduction scheme [t]phi <-> [can(t)]phi, where can(t) is a fixed-order conjunction containing each assigned feature literal once. It denotes the same finite partial assignment u. This explicitly includes elimination of repeated literals. The notation [u]phi is an abbreviation for that conjunction's conditional, not an additional semantic oracle. An auxiliary empty assignment, if used, is identity: [empty]phi <-> phi. It is not identified with a tautological raw antecedent.

### Deterministic assignment rules

For consistent u,v, use

    [u]p <-> 1                if u(p)=1,
    [u]p <-> 0                if u(p)=0,
    [u]p <-> p                if p is not assigned by u,
    [u]NOT phi <-> NOT [u]phi,
    [u](phi AND psi) <-> [u]phi AND [u]psi,
    [u][v]phi <-> [u then v]phi.

Here u then v is the partial assignment with union domain, taking v's value wherever v is defined and u's elsewhere. The symbols 1 and 0 are Boolean truth constants, which can alternatively be defined propositionally. Disjunction and other consequent connectives follow from the Boolean rules.

**Soundness.** Exact De Morgan normalization follows by simultaneously swapping verifier/falsifier families under negation. Conjunction reassociation and commutation follow from compatible union of partial assignments. The inclusive schemes partition the possible exact assignments into the left, right and jointly verified alternatives, including the contextual D fusion. Inconsistent conjunctions have no endpoints. Every consistent assignment has exactly the endpoint w[u], which proves the atomic effect/frame rules, Boolean distribution, and last-write-wins composition. Finally state equivalence is preserved by Boolean contexts and by universal quantification over any fixed antecedent's endpoints.

**Completeness by elimination.** First normalize each antecedent and split disjunctions until all conditions are literal conjunctions. Replace inconsistent ones by TRUE. Normalize nested consequents inside out, using state-context replacement. For consistent assignments, push the operator through Boolean consequents and evaluate its effects on feature atoms; alternatively combine consecutive assignment operators using the composition rule. This yields, by finitely many derivable equivalences, a pure Boolean formula over the original features. A state formula is valid in the full Boolean cube exactly when that resulting Boolean formula is a propositional tautology. Such tautologies are axioms, and the proved equivalence yields the original formula. Hence the calculus is sound and weakly complete. QED.

A nested antecedent is an intervention command, not a state expression to be blindly substituted into. For example p > (NOT p > p) is false: the inner command writes p=0. Naively replacing every occurrence of p by TRUE after the outer command would turn the inner antecedent into FALSE and give an incorrect vacuous truth. Inside-out elimination or command-aware overwrite evaluation avoids this mistake.

This is an actual elimination procedure with concrete intervention rules. It does not assert a Boolean-completion witness as an axiom or take the entire semantic verifier recursion as a theoremhood rule. Its effective completeness is compatible with the preceding no-go because the semantic class has been restricted to value-complete explicit features.

## 5. Logical distinctions and interpretation

The positive restriction retains the intended hyperintensional distinction. At initial p=q=0,

    p > NOT q

is true, while

    (p OR (p AND q)) > NOT q

is false, even though the two antecedents are classically equivalent. The same example distinguishes p from p AND q and refutes unrestricted antecedent strengthening. At p=1, the antecedent p OR NOT p is true but its conditional consequent p can fail, preserving the prior conjunction-conditionalisation counterexample. The earlier export counterexample A=p, B=NOT p OR q, consequent p also lives on this two-feature cube. SDA, MP and one-way import remain sound by restriction of the established model class.

The practical distinction is between “make this observed property true, leaving hidden feature values unconstrained” and “set these explicitly modeled input features to these complete values.” The former may preserve unbounded modal freedom; the latter yields a finite, inspectable intervention program. This is not a causal structural-equation model: downstream causal effects require an additional specified mechanism. No claim of causal identification follows merely from overwrite semantics.

Fixed finite feature sets give a fixed finite state space. The PSPACE and NP/coNP results are uniform in an input-dependent finite number of feature names. They must not be restated as complexity results for unbounded hidden supports, arbitrary domain sizes with opaque predicate tables, or unknown classifiers.

## 6. Relation to existing assignment calculi

DL-PA already studies Boolean assignments and their program combinations. Its complexity was corrected to PSPACE in [BHST14]; the earlier 2013 EXPTIME claim must not be used. The constant-assignment effect/frame and composition rules above are standard dynamic-assignment principles.

There is an even closer existing language: Herzig, Maris and Vianey's DL-PPA [HMV19]. Its states of execution retain both the result valuation and the set of assigned variables, even when a variable is written to its old value. Parallel branches must agree on overlapping writes; inclusive choice permits the left branch, the right branch, or their parallel composition. After linear-size negation normalization, the map

    p -> (p := 1), NOT p -> (p := 0),
    A AND B -> parallel(program(A), program(B)),
    A OR B -> inclusive-choice(program(A), program(B))

is a linear, footprint-preserving translation of exact antecedents into its constant-assignment fragment. Structural induction on the antecedent gives exactly the same consistent partial assignments and endpoints. In particular, p AND NOT p has no successful execution even when one write leaves the original value unchanged: assigned-variable footprints, not just changed-variable sets, determine the conflict. This mechanism is already present in DL-PPA, whose PSPACE results provide additional context for the direct proof above.

The contribution claimed here is the precise semantic restriction and transfer: exact-verifier conjunction is compatible simultaneous assignment, while disjunction includes its fusion alternative. This accounts for the raw language's failure of classical antecedent replacement. Priority for the combined boundary and transfer has not been established; classical assignment-logical results are not claimed as new.

## Reproducible checks

Run `python models/check_interventions.py`. It compares the per-world exact-verifier semantics against an independently implemented normalizer: 12,000 contextual splitting checks, 12,000 nested reduction checks, and 5,832 last-write-wins checks. It also checks 3,200 ordinary QBF translation/world cases, 240 three-variable QBF translations using only positive pair-disjunction antecedents, and 6,912 literal-branch projection checks on a 96-world nontrivial-marker model. These tests support the general proofs; they do not establish undecidability or complexity hardness by enumeration.

## References

- [TW12] N. Troquard and D. Walther, *On satisfiability in ATL with strategy contexts*, Section 4.1, Theorem 1(ii). [Author PDF](https://www.inf.unibz.it/~ntroquard/PAPERS/TrWa12jelia.pdf). Finite S5-product undecidability used in Theorem 1.
- [B12] R. Briggs, *Interventionist Counterfactuals* (2012), Section 4, CM9. [Full text](https://humanities-web.s3.us-east-2.amazonaws.com/philosophy/prod/2024-08/Briggs%20Interventionist%20Counterfactuals%202012.pdf). Its recursive structural-equation semantics differs from the raw Boolean-feature semantics here.
- [BHST14] P. Balbiani, A. Herzig, F. Schwarzentruber and N. Troquard, *DL-PA and DCL-PC: model checking and satisfiability problem are indeed in PSPACE*. [Preprint](https://arxiv.org/abs/1411.7825).
- A. Herzig and A. Saffidine, *A Note on Halpern's Theory of Causality: Structural Equations and Interventions as Dynamic Logic Programs* (2026). [DOI](https://doi.org/10.1007/s10849-026-09468-w). Relevant explicit Boolean intervention-program comparison, not a theorem about hidden arbitrary-support raw models.

- [HMV19] Andreas Herzig, Frédéric Maris and Julien Vianey, *Dynamic Logic of Parallel Propositional Assignments and its Applications to Planning*, IJCAI 2019, 5576–5582. [Proceedings PDF](https://www.ijcai.org/proceedings/2019/0774.pdf), Section 2.2 and Figure 1 (written-variable footprints and compatible parallel execution), Sections 3.3–3.4 (translations and complexity).
