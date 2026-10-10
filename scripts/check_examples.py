#!/usr/bin/env python3
"""Verify explicit manuscript examples and finite construction instances."""
import itertools,json
from pathlib import Path
from check_graphs import nx,switch,certificate,valid_certificate,complementary,encode,ROOT

def covered(g):
    return set(v for s in [[v] for v in g]+[list(e) for e in g.edges()] if certificate(switch(g,s),g) is not None for v in s)==set(g)

def run():
    g=nx.Graph([(0,3),(1,2),(1,3),(2,3)])
    for s in [[0,3],[1,2]]:valid_certificate(g,s,[3,1,2,0])
    assert not complementary(g,1,2)
    house=nx.Graph([(0,1),(0,3),(0,4),(1,2),(2,3),(3,4)])
    successes=[s for s in [[v] for v in range(5)]+[list(e) for e in sorted(house.edges())] if certificate(switch(house,s),house) is not None]
    assert {frozenset(s) for s in successes}=={frozenset([4]),frozenset([0,1]),frozenset([2,3])}
    g=nx.star_graph(4)
    g=nx.relabel_nodes(g,{0:4,4:0})
    g.add_edge(0,1)
    assert sorted(dict(g.degree()).values())==[1,1,2,2,4]
    assert sorted(dict(switch(g,[0]).degree()).values())==[1,2,2,2,3]
    assert not covered(g)
    g=nx.Graph([(0,1),(0,3),(0,5),(1,2),(2,3),(2,4),(2,5),(3,4),(4,5)])
    valid_certificate(g,[3,4],[3,2,1,5,4,0])
    rest=set(g)-{3,4};a=set(g[3])&rest;b=rest-set(g[4])
    assert a=={0,2} and b=={0,1}
    assert not g.has_edge(*a) and g.has_edge(*b)
    out={'graph6':encode(g),'edges':sorted([min(u,v),max(u,v)] for u,v in g.edges()),'switch':[3,4],
         'permutation':[3,2,1,5,4,0], 'H_vertices':sorted(rest),
         'N_x_in_H':sorted(a),'H_minus_N_y':sorted(b),
         'obstruction':'The first set induces no edge; the second induces an edge.'}
    assert out['graph6']=='ElMg'
    valid_certificate(nx.from_graph6_bytes(out['graph6'].encode()),out['switch'],out['permutation'])
    (ROOT/'data/endpoint_exchange_counterexample.json').write_text(json.dumps(out,indent=2)+'\n')
    construction_counts={}
    for m in range(2,5):
        reps=[];pairs=list(itertools.combinations(range(m),2))
        for choices in itertools.product([0,1],repeat=len(pairs)):
            g=nx.Graph();g.add_nodes_from(range(2*m));g.add_edges_from((2*i,2*i+1) for i in range(m))
            for (i,j),t in zip(pairs,choices):g.add_edges_from([(2*i,2*j+t),(2*i+1,2*j+1-t)])
            for i in range(m):
                p=list(range(2*m));p[2*i],p[2*i+1]=p[2*i+1],p[2*i]
                valid_certificate(g,[2*i,2*i+1],p)
            if not any(nx.is_isomorphic(g,h) for h in reps):reps.append(g)
        regular=[nx.from_graph6_bytes(r['graph6'].encode()) for r in json.loads((ROOT/f'data/certificates_n{2*m}.json').read_text()) if r['regular']]
        assert len(reps)==len(regular) and all(any(nx.is_isomorphic(g,h) for h in regular) for g in reps)
        construction_counts[2*m]=len(reps)
    print('Manuscript examples verified; paired construction reproduces regular classes:',construction_counts)
if __name__=='__main__':run()
