#!/usr/bin/env python3
"""Independent graph6 decoder, switcher and exhaustive isomorphism search.
Uses Python's standard library only. Checks every recorded decision and witness.
"""
import collections
import itertools
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def decode(code):
    n=ord(code[0])-63
    assert 0<=n<=8
    bits=[(ord(c)-63)>>k&1 for c in code[1:] for k in range(5,-1,-1)]
    a=[[0]*n for _ in range(n)]
    for bit,(v,u) in zip(bits,((v,u) for u in range(n) for v in range(u))):
        a[u][v]=a[v][u]=bit
    return a

def switched(a,s):
    return [[a[u][v]^int(u!=v and ((u in s)!=(v in s))) for v in range(len(a))] for u in range(len(a))]

def signature(a):
    degrees=list(map(sum,a))
    return tuple(sorted((degrees[u],tuple(sorted(degrees[v] for v,b in enumerate(a[u]) if b))) for u in range(len(a))))

def iso(a,b):
    """Exhaustive bijection search, pruned by degrees and mapped adjacency."""
    n=len(a)
    da=list(map(sum,a));db=list(map(sum,b))
    if sorted(da)!=sorted(db):return None
    ca=[(da[u],tuple(sorted(da[v] for v in range(n) if a[u][v]))) for u in range(n)]
    cb=[(db[u],tuple(sorted(db[v] for v in range(n) if b[u][v]))) for u in range(n)]
    domains=[[v for v in range(n) if ca[u]==cb[v]] for u in range(n)]
    if any(not c for c in domains):return None
    p=[-1]*n;used=set()
    def search():
        if len(used)==n:return p[:]
        best=None
        for u in range(n):
            if p[u]>=0:continue
            choices=[v for v in domains[u] if v not in used and all(a[u][w]==b[v][p[w]] for w in range(n) if p[w]>=0)]
            if not choices:return None
            if best is None or len(choices)<len(best[1]):best=(u,choices)
        u,choices=best
        for v in choices:
            p[u]=v;used.add(v)
            result=search()
            if result is not None:return result
            used.remove(v);p[u]=-1
        return None
    return search()

def witness(a,s,p):
    assert sorted(p)==list(range(len(a)))
    b=switched(a,s)
    assert all(b[u][v]==a[p[u]][p[v]] for u in range(len(a)) for v in range(len(a)))

def main():
    result={}
    summary=json.loads((ROOT/'data/summary.json').read_text())
    for n,expected in [(3,4),(4,11),(5,34),(6,156),(7,1044),(8,12346)]:
        lines=(ROOT/f'data/all_n{n}.g6').read_text().splitlines()
        assert len(lines)==expected
        # Pairwise inequivalence within invariant buckets establishes no repeats.
        buckets=collections.defaultdict(list)
        for code in lines:
            a=decode(code);assert len(a)==n
            bucket=buckets[signature(a)]
            assert all(iso(a,b) is None for b in bucket), ('duplicate',code)
            bucket.append(a)
        audit=[json.loads(x) for x in (ROOT/f'data/audit_n{n}.jsonl').read_text().splitlines()]
        certs=json.loads((ROOT/f'data/certificates_n{n}.json').read_text())
        assert [r['graph6'] for r in audit]==lines
        qualifying=[];switch_count=0;success_count=0
        for r in audit:
            a=decode(r['graph6'])
            edges=[[u,v] for u in range(n) for v in range(u+1,n) if a[u][v]]
            ss=[[u] for u in range(n)]+edges
            assert len(ss)==len(r['outcomes'])
            covered=set();good=[]
            for s,outcome in zip(ss,r['outcomes']):
                switch_count+=1
                b=switched(a,s)
                # Independently evaluate every switch, including prefilter rejections.
                p=iso(b,a)
                assert (p is not None)==isinstance(outcome,list), (n,r['graph6'],s,outcome,p)
                if p is not None:
                    witness(a,s,outcome);covered.update(s);success_count+=1
                    good.append({'vertices':s,'permutation':outcome})
                elif outcome=='edge_count':assert sum(map(sum,a))!=sum(map(sum,b))
                elif outcome=='degree_sequence':assert sorted(map(sum,a))!=sorted(map(sum,b))
                else:assert outcome=='nonisomorphic'
            assert r['qualifies']==(len(covered)==n)
            if len(covered)==n:
                c=certs[len(qualifying)]
                assert c['graph6']==r['graph6'] and c['edges']==edges and c['switches']==good
                assert c['degree_sequence']==sorted(map(sum,a))
                assert c['regular']==(len(set(map(sum,a)))==1)
                seen={0};queue=[0];color={0:0};bipartite=True
                for u in queue:
                    for v in range(n):
                        if not a[u][v]:continue
                        if v not in seen:
                            seen.add(v);queue.append(v);color[v]=1-color[u]
                        elif color[v]==color[u]:bipartite=False
                assert c['connected']==(len(seen)==n)
                # Covered graphs here are connected; the traversal checks all vertices.
                assert len(seen)==n and c['bipartite']==bipartite
                comp=[[int(u!=v)-a[u][v] for v in range(n)] for u in range(n)]
                assert c['self_complementary']==(iso(comp,a) is not None)
                comp_ss=[[u] for u in range(n)]+[[u,v] for u in range(n) for v in range(u+1,n) if comp[u][v]]
                comp_covered=set(v for s in comp_ss if iso(switched(comp,s),comp) is not None for v in s)
                assert c['complement_qualifies']==(len(comp_covered)==n)
                anti=all(any(a[u][v] and all(a[u][w]!=a[v][w] for w in range(n) if w not in (u,v)) for v in range(n) if v!=u) for u in range(n))
                assert c['complementary_edge_cover']==anti
                edge_cover=set(v for sw in good if len(sw['vertices'])==2 for v in sw['vertices'])
                assert c['all_vertices_in_edge_iss']==(len(edge_cover)==n)
                assert min(map(sum,a))+max(map(sum,a))==n
                qualifying.append(r['graph6'])
        assert qualifying==(ROOT/f'data/qualifying_n{n}.g6').read_text().splitlines()
        assert len(qualifying)==len(certs)
        assert summary[str(n)]['graphs']==len(lines)
        assert summary[str(n)]['qualifying']==len(qualifying)
        assert summary[str(n)]['switches_tested']==switch_count
        assert summary[str(n)]['successful_switches']==success_count
        result[n]={'graphs':len(lines),'pairwise_nonisomorphic':True,'switches_rechecked':switch_count,'positive_witnesses_rechecked':success_count,'qualifying':len(qualifying)}
        print(n,result[n],flush=True)
    # Complete labelled search through n=5 checks catalogue coverage without external input.
    for n in range(3,6):
        buckets=collections.defaultdict(list)
        for code in (ROOT/f'data/all_n{n}.g6').read_text().splitlines():
            a=decode(code);buckets[signature(a)].append(a)
        pairs=list(itertools.combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            a=[[0]*n for _ in range(n)]
            for i,(u,v) in enumerate(pairs):a[u][v]=a[v][u]=(mask>>i)&1
            assert any(iso(a,b) is not None for b in buckets[signature(a)])
        result[n]['all_labelled_graphs_covered']=1<<len(pairs)
    nc=json.loads((ROOT/'data/nonclosure.json').read_text())
    a=decode(nc['graph6'])
    witness(a,nc['S'],nc['S_permutation']);witness(a,nc['T'],nc['T_permutation'])
    assert set(nc['symmetric_difference'])==set(nc['S'])^set(nc['T'])
    assert iso(switched(a,nc['symmetric_difference']),a) is None
    assert nc['original_degree_sequence']==sorted(map(sum,a))
    assert nc['composed_degree_sequence']==sorted(map(sum,switched(a,nc['symmetric_difference'])))
    ec=json.loads((ROOT/'data/endpoint_exchange_counterexample.json').read_text())
    a=decode(ec['graph6']);witness(a,ec['switch'],ec['permutation'])
    assert ec['edges']==[[u,v] for u in range(len(a)) for v in range(u+1,len(a)) if a[u][v]]
    x,y=ec['switch'];rest=set(range(len(a)))-{x,y}
    aa={v for v in rest if a[x][v]};bb={v for v in rest if not a[y][v]}
    assert sorted(aa)==ec['N_x_in_H'] and sorted(bb)==ec['H_minus_N_y']
    assert sum(a[u][v] for u in aa for v in aa)!=sum(a[u][v] for u in bb for v in bb)
    (ROOT/'data/verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('All catalogue, decision, coverage and certificate checks passed.')
if __name__=='__main__':main()
