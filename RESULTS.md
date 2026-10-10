# Identity Seidel switches: completed results

We tested every singleton and every adjacent pair in all **13,595** simple graphs up to isomorphism of orders **3 through 8**, including disconnected graphs. There are **63 qualifying graphs**. Every positive switch has an explicit isomorphism permutation, including successful switches of graphs that fail the covering property. The enumeration made **292,423 switch decisions** and found **7,279 positive switches**. A separate exact standard-library implementation independently rechecked every decision and permutation.

The requested deliverables are `note.tex`, `note.pdf`, the `data/` catalogues and certificates, and the reproducible `scripts/` checkers. No email, Mail, or repository operations were performed. The optional Lean extension was omitted; all claimed general results have written proofs, and no new kernel verification is claimed.

## Definition and source

For a finite simple graph G and S contained in V(G), write G^S for the graph formed by toggling all edges across the cut (S,V\S), preserving both induced sides. An identity Seidel switch (ISS) satisfies G^S isomorphic to G. A vertex-ISS is a singleton; an edge-ISS is an **adjacent** pair, as in Gervacio's Section 5. A graph is called **covered** here when every vertex belongs to one of these two kinds of ISS. Isomorphisms are unrestricted permutations of the whole vertex set.

Source read: Severino V. Gervacio, *On identity Seidel switches*, arXiv:2601.04530v1, definitions in Section 4 and Sections 5–6. The paper's group claim is not used. Further source distinctions are recorded below.

## Enumeration

| n | All graphs | Switches tested | Positive switches in all graphs | Covered | Regular covered | Bipartite covered | Covered using edges alone |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 4 | 18 | 6 | 1 | 0 | 1 | 1 |
| 4 | 11 | 77 | 13 | 3 | 1 | 2 | 3 |
| 5 | 34 | 340 | 48 | 3 | 0 | 2 | 2 |
| 6 | 156 | 2106 | 178 | 11 | 2 | 3 | 11 |
| 7 | 1044 | 18270 | 846 | 10 | 0 | 3 | 4 |
| 8 | 12346 | 271612 | 6188 | 35 | 3 | 4 | 35 |

All 63 covered graphs are connected. None is self-complementary, and none has a covered complement. These observations follow from the all-order theorem below, rather than remaining finite conjectures.

At n=3 the graph is K(1,2). At n=4 the graphs are K(1,3), the paw, and C4. At n=5 they are K(1,4), the house, and K(2,3). At n=6 the regular graphs are the triangular prism and K(3,3). At n=8 there are three regular examples. The paired construction below reproduces all regular examples through n=8; completeness of that construction for arbitrary regular members is not asserted.

At n=5 one graph (the house), and at n=7 six graphs, have a vertex in no edge-ISS. Singletons are therefore essential to the requested property. At even order the singleton degree condition is impossible, so edge-ISS alone must cover every vertex.

The following is the full qualifying list through n=6. Vertices are labelled from zero; each edge `uv` joins u and v. The graph6 encodings preserve these labels. All required switch permutations, and the additional orders 7 and 8, are listed in `data/catalogue.md` and the JSON files.

| n | graph6 | Degree sequence | Edges |
|---:|---|---|---|
| 3 | `Bo` | 1, 1, 2 | 01, 02 |
| 4 | `CF` | 1, 1, 1, 3 | 03, 13, 23 |
| 4 | `CN` | 1, 2, 2, 3 | 03, 12, 13, 23 |
| 4 | `Cl` | 2, 2, 2, 2 | 01, 03, 12, 23 |
| 5 | `D?{` | 1, 1, 1, 1, 4 | 04, 14, 24, 34 |
| 5 | `Dlc` | 2, 2, 2, 3, 3 | 01, 03, 04, 12, 23, 34 |
| 5 | `D]o` | 2, 2, 2, 3, 3 | 02, 03, 04, 12, 13, 14 |
| 6 | `E?Bw` | 1, 1, 1, 1, 1, 5 | 05, 15, 25, 35, 45 |
| 6 | `Exe_` | 2, 2, 2, 2, 4, 4 | 01, 02, 04, 05, 12, 23, 25, 34 |
| 6 | `E?~o` | 2, 2, 2, 2, 4, 4 | 04, 05, 14, 15, 24, 25, 34, 35 |
| 6 | `EyuG` | 2, 2, 2, 4, 4, 4 | 01, 02, 04, 05, 12, 13, 14, 34, 45 |
| 6 | `ElfO` | 2, 2, 3, 3, 4, 4 | 01, 03, 04, 05, 12, 15, 23, 34, 35 |
| 6 | `Exf_` | 2, 2, 3, 3, 4, 4 | 01, 02, 04, 05, 12, 15, 23, 25, 34 |
| 6 | `EO~o` | 2, 2, 3, 3, 4, 4 | 02, 04, 05, 14, 15, 24, 25, 34, 35 |
| 6 | `ElMg` | 2, 3, 3, 3, 3, 4 | 01, 03, 05, 12, 23, 24, 25, 34, 45 |
| 6 | `EtTg` | 3, 3, 3, 3, 3, 3 | 01, 02, 03, 14, 15, 23, 25, 34, 45 |
| 6 | `ElUg` | 3, 3, 3, 3, 3, 3 | 01, 03, 05, 12, 14, 23, 25, 34, 45 |
| 6 | `E^mG` | 2, 2, 4, 4, 4, 4 | 02, 03, 04, 05, 12, 13, 23, 24, 34, 45 |

## Cut identity and degree constraints: proofs

Put e_cut = e_G(S,V\S). There are |S|(n-|S|) possible edges across the cut. Switching removes its e_cut present edges and adds its |S|(n-|S|)-e_cut missing edges. Hence

    |E(G^S)| - |E(G)| = |S|(n-|S|) - 2 e_cut.

Isomorphic graphs have equal edge counts. For a singleton S={v}, e_cut=deg(v), giving **2 deg(v)=n-1**. For an adjacent pair S={x,y}, e_cut=deg(x)+deg(y)-2, giving **deg(x)+deg(y)=n**. For a nonadjacent pair the corresponding sum is n-2; such pairs do not count as edge-ISS.

A nonempty graph has every vertex a vertex-ISS exactly when n=1. Indeed, otherwise the singleton condition makes it d-regular with d=(n-1)/2>0. For an edge vw, switching at v changes the degree of w from d to d-1, contradicting regularity of any isomorphic image. At n=1 every switch leaves the graph unchanged. This is the short answer to the source's Problem 6.1.

## Every covered graph satisfies delta + Delta = n

Let h=(n-1)/2. A vertex of degree other than h cannot be a vertex-ISS, so it has an edge-ISS neighbor of degree n minus its own degree.

First Delta>h. Otherwise a vertex of degree below h would require a neighbor above h. Thus all degrees would equal h; no edge could be an edge-ISS, and every vertex would have to be a vertex-ISS, contradicting the preceding proposition.

A vertex of degree Delta therefore has an edge-ISS partner of degree n-Delta, implying delta+Delta<=n. If delta differs from h, a vertex of degree delta also has such a partner, implying delta+Delta>=n. If delta=h, n is odd and the integer Delta>h is at least h+1=n-delta. Equality follows in either case.

Consequences valid for every n>=3:

- **Connectedness.** If disconnected, a component containing a maximum-degree vertex has at least Delta+1 vertices and another component has at least delta+1. The total exceeds n.
- **Complement exclusion.** In the complement the extreme-degree sum is 2(n-1)-(delta+Delta)=n-2, so it cannot be covered.
- **No self-complementary member.** Coverage is preserved by isomorphism, while complementation excludes it.
- **Regular degree.** A regular covered graph has even order and degree n/2.
- **Local degree restriction.** Every vertex whose degree is not (n-1)/2 has an adjacent partner of degree n-d. Consequently, the degree values other than the singleton exception require this reflected value. No equality of their multiplicities is asserted: stars already show why that would fail.

The extremal identity is necessary, not sufficient. Add an edge 01 between two leaves of K(1,4), with center 4. The degree sequence is (1,1,2,2,4), so delta+Delta=5. Vertex 0 has no neighbor of degree 3 for an edge-ISS. Switching at 0 gives degree sequence (1,2,2,2,3), so it is not a vertex-ISS either. This example is checked by `scripts/check_examples.py`.

## Regular graphs: exact local characterization

Call an adjacent pair x,y **complementary outside the pair** if every other vertex sees exactly one of x,y.

A regular graph of order n>=3 is covered if and only if n is even, its degree is n/2, and every vertex has a complementary adjacent partner. Moreover, in a regular covered graph the edge-ISS are precisely these pairs.

Proof: the extreme-degree theorem gives d=n/2 and excludes singleton ISS. If xy is an edge-ISS and an outside vertex w has c neighbors in {x,y}, its switched degree is d+2-2c. It must remain d, so c=1. Conversely, for a complementary adjacent pair the transposition (x y), fixing the other vertices, maps the switched graph to the original. This converse needs no regularity assumption.

Thus regularity does not merely constrain degree sequences: it gives a complete test using external neighborhoods, without general graph-isomorphism searches.

## Bipartite graphs: complete classification

The bipartite covered graphs are exactly K(a,b), with a,b>=1 and a+b=n.

For necessity, connectedness gives a bipartition A,B with 1<=a=|A|<=b=|B|. For any edge-ISS across the bipartition, the degree sum n=a+b forces both endpoints to reach their maximum possible degrees b and a. Take v in B. If it lies in an edge-ISS then deg(v)=a. If it is covered only by a singleton, deg(v)=(n-1)/2<=a<=floor(n/2); integrality forces n odd and a=(n-1)/2, again deg(v)=a. Hence every vertex of B is adjacent to every vertex of A. Conversely, every cross-part pair of K(a,b) is complementary outside the pair, certified by its endpoint transposition.

This explains the observed floor(n/2) bipartite isomorphism classes at each order and gives qualifying graphs for every n>=3.

## Infinite constructions and their limits

**Paired construction.** On 2m vertices, m>=2, take m disjoint adjacent pairs. Between each pair of pairs, choose either of the two perfect matchings. Every vertex has degree m, and each designated pair is complementary outside the pair. The endpoint transpositions give explicit edge-ISS certificates. This includes K(m,m) and two copies of K_m joined by a perfect matching; for m=3 the latter is the triangular prism.

**Independent-set blow-ups.** Suppose every vertex of a base graph has a complementary adjacent partner. Replace each vertex u by a nonempty independent set I_u, with all-or-none adjacency between sets according to the base graph. For a complementary pair u,v, every x in I_u and y in I_v remains complementary: other vertices in these two sets see exactly one endpoint, and other sets inherit the base property. The endpoint transposition is again a certificate. Arbitrary positive multiplicities give further irregular covered graphs.

**Irregular exceptions to the complementary-pair test.** The paw with edges 03,12,13,23 is covered by switches {0,3} and {1,2}, each certified by permutation [3,1,2,0]. The pair {1,2} has common neighbor 3 and common nonneighbor 0; vertices 1 and 2 have no complementary partner. Thus the regular characterization cannot simply be imposed on irregular graphs.

**Mixed coverage.** The house, with edges 01,03,04,12,23,34, has exactly the successful switches {4}, {0,1}, {2,3}. The roof vertex 4 needs the singleton. Certificates are in the order-five data.

The exact classification of arbitrary irregular, nonbipartite covered graphs remains open. The results above settle the bipartite and regular subclasses and prove all-order restrictions and constructions. No finite observation is being asserted as a complete general characterization.

## A minimal failure of ISS composition

Take V={0,1,2} and E={12}, namely K2 plus an isolated vertex.

- S={1}: the switched graph has only edge 01; p=[2,1,0] maps it to G.
- T={2}: the switched graph has only edge 02; p=[1,0,2] maps it to G.
- S symmetric-difference T={1,2}: both 01 and 02 are added and 12 remains, giving K3, not isomorphic to G.

Thus both switches are ISS but their composition is not. The example is minimal: n=1 has only trivial switch operators; at n=2 either singleton changes the edge count and hence is not an ISS. It also works after identifying complementary switch subsets. `data/nonclosure.json` records the edge list and certificates.

The operators satisfy (G^S)^T=G^(S symmetric-difference T) on labelled graphs. Closure of their identity-to-isomorphism family does not follow: a witnessing isomorphism can move the labels of the second subset.

## Additional distinctions in arXiv v1

The paper's definitions agree with the computation, but two additional structural assertions in Section 5 fail under unrestricted graph isomorphism.

1. **Lemma 5.2 (neighborhood partition).** For the paw above, {1,2} is an edge-ISS while its two outside neighborhoods are both {3}, with vertex 0 in neither. They do not form a partition. Its explicit certificate is [3,1,2,0].
2. **Theorem 5.3 (necessity of the endpoint-exchange condition).** Take the six-vertex graph with edges 01,03,05,12,23,24,25,34,45 (graph6 `ElMg`). Switching S={3,4} has certificate p=[3,2,1,5,4,0]. The remaining induced graph is C4 on the cycle 0,1,2,5,0. N(3) in that cycle is {0,2}, a nonedge, while its vertex set minus N(4) is {0,1}, an edge. No automorphism maps the former set to the latter. Thus condition (ii) is not necessary. This counterexample is stored separately and checked directly.

These are concrete distinctions in the fetched first version, not assumptions about a corrected manuscript. The degree-sum statement itself is valid; the cut identity proves it without assuming that an isomorphism preserves the switched pair. Our main arguments and enumeration use none of these failed assumptions.

## Verification and completeness

- Inputs through order seven are NetworkX 3.4.2's `graph_atlas_g`, based on the Read–Wilson atlas. Order eight is McKay's published `graph8.g6` catalogue. The source URL and exact input hashes are in `data/provenance.json`.
- All 13,595 representatives were checked pairwise for nonisomorphism within invariant buckets by the independent checker. A bucket uses degrees and neighbor-degree lists only as necessary invariants; exact bijection search decides collisions.
- Every labelled graph on three, four and five vertices (8, 64 and 1,024 graphs respectively) was matched to a catalogue representative. For orders six through eight, full coverage relies on the published catalogues and their established counts 156, 1,044 and 12,346. Distinctness and counts were verified locally; no claim of enumerating all 268 million labelled order-eight graphs is made.
- The primary enumerator first applies the cut edge count, then the degree multiset, then NetworkX VF2. These are exact tests, and every singleton and original adjacent pair is evaluated, including those of already rejected graphs.
- The separate standard-library checker independently decodes graph6, toggles each cut, and searches all degree-compatible bijections with adjacency pruning. It repeats **all 292,423 decisions**, including every prefilter rejection, and verifies the permutation arrays for all **7,279** successes.
- The explicit examples and finite paired constructions were separately checked. The constructions give all 1, 2 and 3 regular qualifying isomorphism classes at orders 4, 6 and 8.
- `data/verification.json` records the completed independent checks. The LaTeX note is compiled and its rendered pages inspected for layout. No fresh Lean formalization or execution is included.

The public research package is the note, README, results, requirements, scripts, and data. Private correspondence and temporary execution material are outside that package.
