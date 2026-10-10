#!/usr/bin/env python3
"""Exhaustive small-graph ISS enumeration. Single process, exact arithmetic."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import platform
import time
import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {3: 4, 4: 11, 5: 34, 6: 156, 7: 1044, 8: 12346}

def switch(g, subset):
    h = g.copy()
    subset = set(subset)
    for u in subset:
        for v in set(g) - subset:
            if h.has_edge(u, v):
                h.remove_edge(u, v)
            else:
                h.add_edge(u, v)
    return h

def certificate(h, g):
    """Return p mapping h to g; None is an exhaustive VF2 rejection."""
    if sorted(dict(h.degree()).values()) != sorted(dict(g.degree()).values()):
        return None
    matcher = nx.algorithms.isomorphism.GraphMatcher(h, g)
    if not matcher.is_isomorphic():
        return None
    return [matcher.mapping[v] for v in range(len(g))]

def valid_certificate(g, subset, p):
    n = len(g)
    assert sorted(p) == list(range(n))
    for u in range(n):
        for v in range(u + 1, n):
            assert (g.has_edge(u, v) ^ ((u in subset) != (v in subset))) == g.has_edge(p[u], p[v])

def encode(g):
    # graph6 labels follow node insertion order; preserve numeric vertex labels.
    assert set(g) == set(range(len(g)))
    ordered = nx.Graph()
    ordered.add_nodes_from(range(len(g)))
    ordered.add_edges_from(g.edges())
    return nx.to_graph6_bytes(ordered, header=False).decode().strip()

def complementary(g, u, v):
    return all(g.has_edge(u, w) != g.has_edge(v, w) for w in g if w not in (u,v))

def main(max_n):
    data = ROOT / 'data'
    data.mkdir(exist_ok=True)
    atlas = nx.graph_atlas_g()
    summary = {}
    for n in range(3, max_n + 1):
        start = time.monotonic()
        path = data / f'all_n{n}.g6'
        if n <= 7:
            path.write_text(''.join(encode(g) + '\n' for g in atlas if len(g) == n))
        lines = path.read_text().splitlines()
        assert len(lines) == EXPECTED[n] and len(set(lines)) == len(lines)
        records, audit = [], []
        stats = collections.Counter()
        for code in lines:
            g = nx.from_graph6_bytes(code.encode())
            assert len(g) == n
            edges = sorted([min(u,v), max(u,v)] for u,v in g.edges())
            subsets = [[v] for v in g] + edges
            successes, outcomes = [], []
            covered = set()
            for s in subsets:
                stats['switches_tested'] += 1
                cut = sum(g.has_edge(u,v) for u in s for v in g if v not in s)
                if 2 * cut != len(s) * (n - len(s)):
                    outcomes.append('edge_count')
                    stats['edge_count_rejections'] += 1
                    continue
                h = switch(g,s)
                if sorted(dict(h.degree()).values()) != sorted(dict(g.degree()).values()):
                    outcomes.append('degree_sequence')
                    stats['degree_sequence_rejections'] += 1
                    continue
                p = certificate(h,g)
                if p is None:
                    outcomes.append('nonisomorphic')
                    stats['isomorphism_rejections'] += 1
                    continue
                valid_certificate(g,s,p)
                outcomes.append(p)
                successes.append({'vertices': s, 'permutation': p})
                covered.update(s)
                stats['successful_switches'] += 1
            qualifies = len(covered) == n
            audit.append({'graph6':code, 'outcomes':outcomes, 'qualifies':qualifies})
            if qualifies:
                deg = sorted(dict(g.degree()).values())
                comp = nx.complement(g)
                comp_covered = set()
                for s in [[v] for v in g] + [list(e) for e in comp.edges()]:
                    if certificate(switch(comp,s),comp) is not None:
                        comp_covered.update(s)
                record = {'graph6':code,'n':n,'edges':edges,'degree_sequence':deg,
                    'switches':successes,'regular':len(set(deg))==1,
                    'connected':nx.is_connected(g),
                    'bipartite':nx.is_bipartite(g),
                    'self_complementary':nx.is_isomorphic(g,comp),
                    'complement_qualifies':len(comp_covered)==n,
                    'complementary_edge_cover':all(any(g.has_edge(u,v) and complementary(g,u,v) for v in g if v!=u) for u in g),
                    'all_vertices_in_edge_iss':set(v for sw in successes if len(sw['vertices'])==2 for v in sw['vertices']) == set(g)}
                records.append(record)
        (data / f'qualifying_n{n}.g6').write_text(''.join(r['graph6']+'\n' for r in records))
        (data / f'certificates_n{n}.json').write_text(json.dumps(records,indent=2)+'\n')
        (data / f'audit_n{n}.jsonl').write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in audit))
        row = dict(stats)
        row.update(graphs=len(lines), qualifying=len(records), regular=sum(r['regular'] for r in records),
                   connected=sum(r['connected'] for r in records),
                   bipartite=sum(r['bipartite'] for r in records),
                   self_complementary=sum(r['self_complementary'] for r in records),
                   complement_qualifies=sum(r['complement_qualifies'] for r in records),
                   complementary_edge_cover=sum(r['complementary_edge_cover'] for r in records),
                   all_vertices_in_edge_iss=sum(r['all_vertices_in_edge_iss'] for r in records),
                   seconds=round(time.monotonic()-start,3))
        summary[n]=row
        print(n,json.dumps(row),flush=True)
    (data/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    provenance = {'python':platform.python_version(),'networkx':nx.__version__,
        'inputs':{f'all_n{n}.g6':{'sha256':hashlib.sha256((data/f'all_n{n}.g6').read_bytes()).hexdigest(),
            'source': 'NetworkX graph_atlas_g (Read-Wilson atlas)' if n<=7 else 'https://users.cecs.anu.edu.au/~bdm/data/graph8.g6'} for n in summary},
        'certificate_convention':'p[i] is the image of vertex i under an isomorphism G^S -> G',
        'audit_order':'singletons 0..n-1, then original edges in lexicographic order'}
    (data/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-n',type=int,default=8,choices=range(3,9))
    main(parser.parse_args().max_n)
