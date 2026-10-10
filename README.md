# Vertex and edge identity Seidel switches

This package studies finite simple graphs in which every vertex belongs to an identity Seidel switch (ISS) that is either a singleton or an adjacent pair. It contains exhaustive results for all graphs up to isomorphism on three through eight vertices, explicit isomorphism certificates, and proofs valid at every order.

An ISS is a subset `S` for which toggling all adjacencies between `S` and its complement gives a graph isomorphic to the original. An edge-ISS must be an **edge of the original graph**. The isomorphism may move any vertex. No closure of the ISS family under composition is assumed.

## Results

| Order | Input graphs | Qualifying graphs |
|---:|---:|---:|
| 3 | 4 | 1 |
| 4 | 11 | 3 |
| 5 | 34 | 3 |
| 6 | 156 | 11 |
| 7 | 1,044 | 10 |
| 8 | 12,346 | 35 |

Every qualifying graph is connected and satisfies `minimum degree + maximum degree = order`. Its complement never qualifies. The qualifying bipartite graphs are exactly the complete bipartite graphs. The note gives a characterization of the regular members and further infinite constructions. The unrestricted irregular case remains open.

- `note.pdf`, `note.tex`: short mathematical note by Haobo Ma and Wenlin Zhang.
- `RESULTS.md`: proofs, detailed findings, source distinctions and verification scope.
- `data/qualifying_nN.g6`: one graph6 representative of every qualifying graph of order `N`.
- `data/certificates_nN.json`: edge lists, degree sequences, structural properties, and **every successful singleton and edge switch** for each qualifying graph.
- `data/catalogue.md`: human-readable edge lists and certificates for all 63 qualifying graphs.
- `data/all_nN.g6`: complete input catalogues, including disconnected graphs.
- `data/audit_nN.jsonl`: every tested switch decision for every input graph, with witnesses for successes even in nonqualifying graphs.
- `data/summary.json`, `data/verification.json`: enumeration and independent verification counts.
- `data/provenance.json`: input sources, software versions and SHA-256 hashes.
- `data/nonclosure.json`: minimal counterexample to closure under composition.
- `data/endpoint_exchange_counterexample.json`: counterexample to the endpoint-exchange condition in the source's Theorem 5.3.

## Reproduce

Python 3.10 or later is sufficient. The enumerator uses NetworkX 3.4.2. All scripts run sequentially in one process; no workers are created.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/check_graphs.py
python3 scripts/verify.py
.venv/bin/python scripts/check_examples.py
```

The enumerator regenerates the order-three-through-seven input from the NetworkX graph atlas; the bundled order-eight input is used directly. To obtain that input afresh:

```sh
curl -L --fail https://users.cecs.anu.edu.au/~bdm/data/graph8.g6 -o data/all_n8.g6
```

`verify.py` uses **only the Python standard library** and requires no installation. It independently implements graph6 decoding, cut toggling and exact bijection search. It reevaluates every switch, verifies the positive permutations, checks the qualifying lists, and checks pairwise nonisomorphism of all input representatives. It additionally matches every labelled graph through order five to the input catalogue. Completeness at orders six through eight relies on the cited published catalogues, with verified distinct representative counts. `check_examples.py` verifies the manuscript's explicit counterexamples and the paired construction through order eight.

Compile the note with two passes:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

## Certificate and audit conventions

Vertices are integers `0, ..., N-1`. A permutation array `p` is in **image notation**, not cycle notation: `p[i]` is the image of vertex `i` under an isomorphism **from the switched graph to the original graph**. Verification requires, for every distinct `u,v`,

```text
(original_edge(u,v) XOR (exactly one of u,v belongs to S))
    == original_edge(p[u],p[v]).
```

In each audit row, `outcomes` first lists the singletons `[0], ..., [N-1]`, followed by all original edges `[u,v]`, `u<v`, in lexicographic order. An array is a successful isomorphism certificate. Other values are `edge_count`, `degree_sequence`, or `nonisomorphic`; each denotes an exact rejection. A necessary-condition rejection is a complete mathematical test of that switch, not a skipped case. Every switch is evaluated even after a graph is known not to qualify.

A graph6 string is a representative encoding, **not a canonical identifier** independent of labelling. Different graph6 strings can describe isomorphic graphs; the verifier checks actual isomorphism, not string equality, when establishing distinctness. JSON has the usual escaping for backslashes in graph6 strings.

`complementary_edge_cover` means every vertex has an adjacent partner such that every vertex outside that pair sees exactly one endpoint. It is a sufficient condition in general and the exact edge-ISS condition in a regular covered graph. It is not assumed for the general enumeration.

## Sources and scope

- Severino V. Gervacio, *On identity Seidel switches*, [arXiv:2601.04530v1](https://arxiv.org/abs/2601.04530v1), especially the definitions and Sections 5–6.
- R. C. Read and R. J. Wilson, *An Atlas of Graphs*, Oxford University Press, 1998; distributed through NetworkX's `graph_atlas_g`.
- Brendan D. McKay, [Graphs data catalogue](https://users.cecs.anu.edu.au/~bdm/data/graphs.html), order-eight graph6 list.

The proofs are written mathematical arguments; no new Lean formalization is included. The source's ISS group assertion is not used. Explicit source counterexamples are recorded in the note and results.

For a public repository, the self-contained research package is `README.md`, `RESULTS.md`, `note.tex`, `note.pdf`, `requirements.txt`, `scripts/`, and `data/`. Private task correspondence, runtime logs, the local virtual environment and temporary working files are not part of that package. No repository operation is required to run or verify it.
