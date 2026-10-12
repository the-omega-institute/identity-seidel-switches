# Essential singleton Seidel switches

This folder contains the reviewed [note](note.pdf), its [LaTeX source](note.tex),
and a reproducible numerical check of the results following Severino V.
Gervacio's question of 12 October 2026. It uses only this checkout and two
checksum-pinned public data downloads; no sibling research directories are needed.

A Seidel switch at a set `S` toggles the edges between `S` and its complement.
It is an identity Seidel switch (ISS) when the switched graph is isomorphic to
the original. A graph is **covered** when every vertex belongs to a singleton
ISS or an ISS consisting of an original edge's endpoints. Write `W` for the
singleton-ISS vertices, `P` for the graph of edge-ISS pairs, and `U` for the
isolated vertices of `P`. In a covered graph, the vertices of `U` require
singleton switches.

## Proved in the note

- A switching isomorphism at a singleton vertex maps that vertex into `W`.
  In particular, if `W = {v}`, every switching isomorphism at `v` fixes `v`.
  The transport lemma also relates singleton switches before and after
  switching and counts the edge-ISS partners of a singleton vertex.
- For a graph of order `2h+1`, with `h >= 1` and all degrees in `{h,h+1}`,
  an essential singleton forces `W = {v}`. Every switching isomorphism at
  that vertex fixes it. In this degree range, an original edge is an ISS
  exactly when each outside vertex sees exactly one endpoint.
- For every simple graph `F` on `m >= 2` vertices, the construction `C(F)`
  is covered and has degrees `m` and `m+1`. The note determines all its
  singleton and edge switches. If `F` has no isolated vertices, then
  `U = W = {v}`; otherwise `U` is empty. Nonisomorphic bases without
  isolated vertices give nonisomorphic constructed graphs. The family
  starts with the house and gives an essential singleton at every odd
  order at least five.

These are written mathematical proofs; this package contains no Lean
formalization. The arguments do not assume that ISS subsets form a group.

## Computed results

The exhaustive enumeration includes disconnected graphs and tests every
singleton and every original edge, using cut-edge counts and degree invariants
for necessary rejections, followed by exact bijection search. It reproduces:

| Order | Input isomorphism classes | Covered | `U` empty | `|U| = 1` |
|---:|---:|---:|---:|---:|
| 3 | 4 | 1 | 1 | 0 |
| 4 | 11 | 3 | 3 | 0 |
| 5 | 34 | 3 | 2 | 1 |
| 6 | 156 | 11 | 11 | 0 |
| 7 | 1,044 | 10 | 4 | 6 |
| 8 | 12,346 | 35 | 35 | 0 |
| 9 | 274,668 | 33 | 17 | 16 |

No covered graph in these orders has `|U| >= 2`. In all 23 essential-singleton
cases, `U = W = {v}` and every switching isomorphism at `v` fixes it. Through
order seven, a separate check of all `n!` permutations confirms the essential
vertices' isomorphism counts. The transport lemma is checked on every
singleton switching isomorphism through order seven, including uncovered
graphs (1,757 checks). All 1,098 labelled base graphs of orders two through
five are used to check the complete switch lists of `C(F)`.

The scripts also check the small orders: the one-vertex graph is covered
with `U = W = V`, and the only covered two-vertex graph is `K2`, with `U` empty.
Catalogue completeness relies on the cited published input catalogues.

## Open questions

For arbitrary covered graphs with `|U| = 1`, must `W` also consist of that
single vertex, or must there at least exist a switching isomorphism fixing
it? Can a covered graph have `|U| >= 2`, and which induced graphs on `U` can
occur? The theorem settles the fixing question in the stated two-degree
range; the finite computations do not settle it at all orders.

## Reproduce

Use Python 3.10 or later on macOS or Linux. Only the standard library is
needed; no NetworkX installation is required. From the repository root:

```sh
python3 essential-singletons/scripts/reproduce.py
```

This is the complete numerical reproduction command. It runs sequentially in
one Python process, creates no workers, checks peak RSS is below 1,000,000,000
bytes, and prints the measured peak to the terminal. Do not use Python's `-O`
option: the checker uses assertions. All paths are resolved from the scripts,
so the command also works from another working directory when the script is
addressed by its absolute path.

On the first run, it downloads the order-nine graph6 file and the NetworkX
3.4.2 atlas into the ignored `essential-singletons/.cache/` directory. Every
use checks the recorded SHA-256, including cached files; a mismatch fails the
run. Delete the affected cached file to request a fresh download. Subsequent
runs need no network connection once both verified inputs are cached.
The scripts never download citation PDFs or live documentation pages.

The stages can also be run separately, in this order:

```sh
python3 essential-singletons/scripts/check_sources.py
python3 essential-singletons/scripts/independent_review.py
python3 essential-singletons/scripts/check_atlas.py
```

The first stage verifies all input hashes. The second recomputes the graph
catalogues, certificates, isomorphism counts, transport checks, and construction
checks against the checked-in reviewed results, then rewrites identical
numerical JSON. The third checks the atlas against the local inputs, the
order-nine essential-switch certificates, and the two order-seven construction
identifications. Keep the checked-in JSON in place: it supplies the expected
results. `reproduce.py` additionally checks the table above, the unchanged
note's hashes, and refreshes the numerical summary and artifact hashes in
`data/final_checks.json`.

To compile the note separately, with a LaTeX installation providing its
listed packages, keep auxiliary files in the ignored cache:

```sh
mkdir -p essential-singletons/.cache/tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=essential-singletons/.cache/tex essential-singletons/note.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=essential-singletons/.cache/tex essential-singletons/note.tex
```

Compilation is separate from the single-process numerical check. The bundled
PDF remains the reviewed artifact; a fresh TeX build need not be byte-identical.

## Inputs, provenance, and output conventions

- Orders 3–7 use the existing top-level `data/all_n3.g6` through
  `data/all_n7.g6`, from the Read–Wilson *Atlas of Graphs* as distributed by
  NetworkX. The downloaded NetworkX 3.4.2 atlas is compared entry by entry,
  in the same order, against these files; it contains 1,253 graphs in total.
- Order 8 uses the existing top-level `data/all_n8.g6` from
  [Brendan McKay's graph catalogue](https://users.cecs.anu.edu.au/~bdm/data/graphs.html).
  Hashes for all local input files are in the top-level `data/provenance.json`.
- Order 9 uses McKay's
  [graph9.g6](https://users.cecs.anu.edu.au/~bdm/data/graph9.g6), containing
  274,668 graphs. Its SHA-256 is
  `839f67ecc73b1f539128694badebe27adf4f0fb1ee6d0663b7ad9868100d5123`.
- The atlas download is
  [atlas.dat.gz at NetworkX 3.4.2](https://raw.githubusercontent.com/networkx/networkx/networkx-3.4.2/networkx/generators/atlas.dat.gz),
  with SHA-256 `73fc416df0164923607751cb759f4ae81deb5f6550bf25be59c86de3b747e41d`.
  Both download URLs and expected hashes are recorded in `data/sources.json`.
  That manifest also preserves historical bibliographic retrieval metadata;
  those HTML/PDF entries are citations, not computational inputs, and their
  old HTTP statuses are not new availability checks.

`data/covered_n1.json` through `data/covered_n9.json` contain every covered
graph's graph6 encoding, degrees, `W`, `P`, `U`, and switch certificates.
Vertices are numbered from zero; `permutation[i]` is the image of vertex `i`
under an isomorphism **from the switched graph to the original graph**.
Graph6 labels are representative encodings, not labelling-independent
canonical identifiers. `data/independent_review.json` contains the complete
numerical summary and essential-vertex isomorphism counts.
`data/atlas_and_certificates.json` records the atlas and additional
certificate checks. Generated JSON contains no machine paths, timings, RSS
measurements, or machine-specific Python version.

`data/final_checks.json` distinguishes the current numerical rerun from the
historical review of the unchanged note. The old review also mentioned an
uncovered order-21 example whose graph input was not supplied in this
checkout. Its result is retained explicitly as historical and **not rerun**;
it is not used in the note or in the reproduced results above. The old
cross-checks against unavailable sibling review files now use the bundled
reviewed catalogues and report instead.

Only the authors' note is bundled as a PDF in this folder. Third-party
copyrighted reference PDFs are not included or downloaded.
