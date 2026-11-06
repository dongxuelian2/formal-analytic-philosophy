# Colored Boolean completion is NP-complete

This note concerns a finite, explicitly given world set and atomic truth/conditional data. It does not assert decidability of an infinite formula profile or an infinite-world representation theorem. The representation class and Boolean-completion criterion are those of [the intrinsic representation note](intrinsic-finite-representation.md).

## 1. The finite decision problem

**CBC.** Input: a nonempty finite set W, equivalence relations E_p on W, and truth sets P_p. Question: does there exist a bounded Boolean sublattice B of Eq(W), with bottom equality and top the universal relation, whose members commute under relational composition, containing every E_p, and such that the Boolean complement of E_p is contained in the equivalence relation of agreement on membership in P_p?

The associated atomic conditionals are explicitly

R_p = E_p intersect (W times P_p),
R_not-p = E_p intersect (W times (W minus P_p)).

Consequently CBC is exactly the atomic-extension problem for the local exact-verifier/raw-variation class, after checking atomic endpoint filtering. All relations and truth sets are explicit, not succinctly encoded.

**Theorem 1.** CBC is NP-complete under polynomial-time many-one reductions. Hardness holds with only two distinct support equivalences E and F, each having exactly two classes, such that each intersection of an E-class with an F-class has the same size K. The uncolored geometry already has a product representation; each support type, with all its truth labels jointly, is individually representable. The number of propositional truth atoms (bits) is part of the input; this is not a claim about an unbounded number of coordinate factors.

With at most one distinct support equivalence, CBC is in P: compare the joint truth-color histograms of its classes, as in Proposition 3 of the intrinsic note. Thus the jump from one to two support types already permits NP-completeness. This does not claim hardness with two propositional atoms.

Membership in NP follows from the polynomial product certificate in the intrinsic note. In brief, discard singleton factors and guess at most floor(log_2 |W|) finite factors, a bijection from W to their product, and a support mask for each atom. Check that E_p is exactly agreement outside its mask, and that P_p is constant on agreement on its mask. These checks are polynomial in the explicit input size. The remainder gives the full hardness reduction.

## 2. A direct criterion for the two-support fork

Fix K >= 1 and W = [K] times {0,1} times {0,1}, with coordinates written (t,x,y). Let

- E relate worlds with the same y;
- F relate worlds with the same x.

All atoms have support relation E or F, with at least one atom of each type. Let alpha(w) be the vector of truth values of all E-type atoms, and beta(w) the vector for all F-type atoms. Regard these vectors as finite colors. In cell (x,y), let M_xy(a,b) be the number of worlds having alpha-color a and beta-color b. Each M_xy has total K.

**Lemma 2 (four marginal criterion).** CBC holds if and only if there is a multiset of K quadruples (a_0,a_1,b_0,b_1) such that, for each x,y, its (a_x,b_y)-marginal is M_xy.

Equivalently, there are nonnegative integers z(a_0,a_1,b_0,b_1) with these four specified pair marginals. This is a direct finite integer-feasibility criterion, with no quantification over equivalence-relation completions. Colors not observed in the input need not be included. Using the unions of the observed alpha and beta alphabets, there are at most |W|^4 variables.

**Proof.** First suppose a completion exists. The intrinsic product theorem gives a product representation. Group its nontrivial coordinates by their membership profiles in the supports of E and F: in both, in E only, in F only, or in neither. E join F is universal, so the last group is trivial. The resulting three factors will be called S, X, Y. Since E has two classes, |Y|=2; since F has two classes, |X|=2. The E meet F classes have size K, so |S|=K. Identify the two X values with the original F-classes x=0,1 and the two Y values with the original E-classes y=0,1.

All E-type truth labels are independent of Y, hence alpha = a_x(s). All F-type labels are independent of X, hence beta = b_y(s). The K values of s give the required quadruples. This argument allows arbitrary refinements of the hidden coordinates; such refinements cannot escape the criterion.

Conversely, enumerate K quadruples realizing the marginals. For each cell (x,y), match its K original worlds to the K quadruple indices s by their pair colors (a_x(s),b_y(s)). Equal multiplicities guarantee a bijection, including repeated colors. The four cell bijections together identify W with [K] times {0,1} times {0,1}. E and F become the claimed support relations, alpha depends only on (s,x), and beta only on (s,y). All truth labels therefore satisfy locality, and the full coordinate Boolean lattice is a valid completion. QED.

After division by K, the four matrices are pair distributions, and the quadruples are deterministic global assignments. This is closely related to the joint-distribution/local-hidden-variable perspective of Fine [F82]. Here the required distribution is an empirical distribution on exactly K equally weighted records: integer multiplicities are essential. Feasibility of an arbitrary real-valued global distribution cannot replace this condition without a separate integrality argument. In fact the real relaxation here has only r^2 s^2 variables for explicitly listed color alphabets of sizes r and s, so it is a polynomial-size linear program. The hardness below is about integer realization at the prescribed total K, not the complexity of that real relaxation. The lemma proves the specific translation to colored equivalence completion.

The lemma also provides a parameter-sensitive algorithm. If the two color alphabets have sizes r and s, enumerating the nonnegative integers z up to K takes at most (K+1)^(r^2 s^2) trials, with polynomial verification. In particular the fork fragment is polynomial-time decidable for a fixed total number of Boolean atoms. This algorithm is not claimed efficient when the number of atoms grows.

## 3. Complete reduction from partial Latin square completion

We use the classical NP-complete problem of completing a partial Latin square of its given order, proved by Colbourn [C84]. No hardness assumption about binary-encoded large numerical margins is needed.

Let L be a valid partial Latin square of order n, given as an explicit n-by-n array of blanks or symbols: its filled entries are symbols in [n], with no repeated symbol in a row or column. Let K be its number of unfilled cells. If K=0, output the fixed YES fork with K=1 and one constantly true atom of each support type; it still has two distinct equivalences, each with two classes. Otherwise define three 0/1 matrices:

- U(a,b)=1 exactly when row a, column b is unfilled;
- V(a,c)=1 exactly when symbol c has not yet appeared in row a;
- T(b,c)=1 exactly when symbol c has not yet appeared in column b.

Each matrix has total K. Their one-dimensional margins agree: for example, sum_b U(a,b) = sum_c V(a,c), the number of blanks in row a. Write d(a) for this number.

A completion of L is equivalent to a nonnegative integer table q(a,b,c) satisfying

sum_c q(a,b,c)=U(a,b),
sum_b q(a,b,c)=V(a,c),
sum_a q(a,b,c)=T(b,c).

Indeed, a completion supplies one triple per previously empty cell. Conversely U forces exactly one symbol in every empty cell and none in a filled cell. V and T force each missing row-symbol and column-symbol pair to occur exactly once. Thus the original entries together with these triples form a Latin square. This proves both directions, rather than appealing to a separate contingency-table hardness theorem.

Now construct the fork W=[K] times {0,1} times {0,1}. Give its four cells these joint color multisets:

- M_00(a,a') = d(a) if a=a', and 0 otherwise;
- M_01(a,c) = V(a,c);
- M_10(b,a) = U(a,b);
- M_11(b,c) = T(b,c).

The color alphabets can all be [n]; the roles A, B, C are distinguished by the cell position, not by unbounded primitive truth values. Materialize each list of K pairs in any fixed order. Encode each alpha color by max(1,ceil(log_2 n)) Boolean truth bits, all with relation E; encode each beta color by the same number of bits, all with relation F. This is a valid instance of the original Boolean-atom problem, not an expansion to multivalued atoms. Define the positive and negative atomic relations by endpoint filtering if conditional relations, rather than E and P, are the required input format.

By Lemma 2 the instance is completable exactly when the four pair multisets are realized by K quadruples. The diagonal marginal M_00 forces a_0=b_0 in every quadruple. Hence each quadruple is exactly a triple (A,B,C)=(a_0,a_1,b_1), and its three other pair marginals are U,V,T. Their multiplicities define q, and conversely any q supplies the quadruples. Combining the two equivalences proves

L is completable iff the constructed CBC instance is YES.

The construction uses 4K <= 4n^2 worlds and O(log n) Boolean atoms. Even explicitly writing every atomic relation matrix takes only polynomial size, O(n^4 log n). K is the number of blanks, not a binary-encoded potentially exponential number. A malformed partial square can be rejected directly and mapped to a fixed NO instance; alternatively the standard NP-complete problem is restricted to valid partial Latin squares. This completes the many-one reduction and Theorem 1. QED.

The promise that each support type separately is representable also holds. For alpha, its joint color histogram across the E-class y=0 is the A-marginal of M_00 plus the B-marginal of M_10. Across y=1 it is the A-marginal of M_01 plus the B-marginal of M_11. These are equal by consistency of U,V,T. The beta comparison across the two F-classes is identical. The single-support histogram criterion applies to all bits jointly. Thus the obstruction is simultaneous alignment, not bad marginal counts for an individual support type.

## 4. A small simultaneous-alignment obstruction

The following is the standard Popescu–Rohrlich (PR-box) parity pattern [PR94], recast as a colored-completion obstruction, not a new parity example. For a fixed NO instance take K=2, alpha(t,x,y)=t and beta(t,x,y)=t XOR (x AND y), one Boolean atom of each support type. Every cell contains one world of each alpha color and one of each beta color; every support type separately passes its histogram test. Three cells require equal alpha/beta, and the fourth requires unequal colors. Any quadruple satisfying the first three would have a_0=b_0=a_1=b_1, contradicting the fourth. Thus no common completion exists. Its eight worlds already have standard uncolored product geometry.

## 5. Consequences and boundaries

1. **Atomic extension is NP-complete.** Given explicit atomic truth and positive/negative conditional relations, deciding existence of a full local exact-verifier/raw-variation extension is NP-complete. Endpoint filtering is polynomial; the reduction always satisfies it. When an extension exists, its endpoint relations for all normal antecedents remain uniquely determined by the intrinsic bilateral recursion. Existence is hard even though the extension is rigid.
2. **Finite observed realization is NP-complete.** The NP upper bound in the intrinsic note now has a matching lower bound: atomic-only observations already suffice. This concerns a finite explicit list of observations, not an arbitrary oracle supplying infinitely many formula relations.
3. **No general polynomial criterion unless P=NP.** A polynomially computable necessary-and-sufficient test for CBC would imply P=NP. The result does not rule out finite structural characterizations, exponential algorithms, useful tractable fragments, or a logical axiomatization with expensive decision procedures.
4. **The difficulty persists with supplied uncolored geometry.** The reduction supplies standard E,F on K times 2 times 2. It asks whether the given colors can be made local by another product identification preserving E,F. If the actual full coordinate identification were fixed and not allowed to change, locality would instead be a direct polynomial check. These are different problems.
5. **Novelty boundary.** Partial Latin square hardness, marginal-table feasibility, joint-distribution/local-hidden-variable viewpoints, the PR-box parity obstruction, and finite factor-equivalence/product decompositions are classical. The contribution here is the explicit polynomial reduction transporting that hardness into the precisely defined colored-completion problem, with the two-support restriction and individual-representability promise. Priority for this combined statement has not been established.

## Reproducible finite checks

Run `python models/check_completion.py` from the repository root. The script compares the four-marginal criterion with direct cellwise coordinate relabelings on all 10,256 binary-color fork instances with K=1 or K=2. It also checks every valid partial Latin square of orders 1, 2, 3: 11,813 inputs, of which 5,869 are completable. A separate sample of 176 positive instances checks the actual Boolean product certificates and atom locality, including zero-blank boundary cases. These finite checks supplement the general proof; they are not the proof of NP-hardness.

## References

[C84] C. J. Colbourn, “The complexity of completing partial Latin squares,” Discrete Applied Mathematics 8(1), 25–30 (1984). [Publisher](https://doi.org/10.1016/0166-218X(84)90075-1). The NP-completeness of the source problem is explicitly stated in the publisher abstract and the author's university record. The reduction above is independent of the details of Colbourn's reduction.

[IJ94] R. W. Irving and M. R. Jerrum, “Three-dimensional statistical data security problems,” SIAM Journal on Computing 23(1), 170–184 (1994). [DOI](https://doi.org/10.1137/S0097539790191010). Section 4.1 defines feasibility with all two-dimensional margins specified and no individual cells prescribed. Corollary 4.2 proves NP-completeness even when every margin entry is 0 or 1. This is prior work, not a result of this note. It is not needed as a hardness premise here, since all numerical sizes are controlled directly by the partial Latin square construction.

For the earlier factor-equivalence, independence, agreement-modal, and assignment/update literature, see the source audit in [the intrinsic note](intrinsic-finite-representation.md). This result neither replaces that attribution nor certifies priority.

[F82] A. Fine, “Hidden Variables, Joint Probability, and the Bell Inequalities,” Physical Review Letters 48, 291–295 (1982). [Publisher full text](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.48.291/fulltext). Relevant joint-distribution perspective, not an integer-realization theorem.

[PR94] S. Popescu and D. Rohrlich, “Quantum Nonlocality as an Axiom,” Foundations of Physics 24, 379–385 (1994). [DOI](https://doi.org/10.1007/BF02058098). Source of the standard nonlocal-box parity pattern.
