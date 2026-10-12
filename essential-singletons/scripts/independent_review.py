#!/usr/bin/env python3
"""Independent exact bitset implementation. No imports from reviewed programs.
One process; streaming graph6; only necessary cut-count/degree rejection.
"""
from collections import Counter
from itertools import combinations, permutations
import hashlib, json, math, resource, sys, time
from inputs import ROOT, graph_input
LIMIT = 1_000_000_000

def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform=='darwin' else 1024)

def decode(s):
    s=s.strip(); n=ord(s[0])-63
    assert 0<=n<=62 and len(s)==1+(n*(n-1)//2+5)//6
    a=[0]*n; t=0
    for j in range(1,n):
        for i in range(j):
            if (ord(s[1+t//6])-63) & (1 << (5-t%6)):
                a[i] |= 1<<j; a[j] |= 1<<i
            t+=1
    return tuple(a)

def encode(a):
    bits=[]
    for j in range(1,len(a)):
        bits.extend((a[i]>>j)&1 for i in range(j))
    bits += [0]*((-len(bits))%6)
    return chr(len(a)+63)+''.join(chr(63+sum(bits[k+t]<<(5-t) for t in range(6))) for k in range(0,len(bits),6))

def switch(a,s):
    mask=sum(1<<v for v in s); outside=((1<<len(a))-1)^mask
    return tuple(row ^ (outside if mask&(1<<v) else mask) for v,row in enumerate(a))

def valid(a,b,p):
    n=len(a)
    return sorted(p)==list(range(n)) and all(((a[i]>>j)&1)==((b[p[i]]>>p[j])&1) for i in range(n) for j in range(i))

def maps(a,b,fixed=None):
    n=len(a); da=[r.bit_count() for r in a]; db=[r.bit_count() for r in b]
    if sorted(da)!=sorted(db): return
    # Degree and sorted neighbor-degree multisets are isomorphism invariants.
    sa=[(da[i],tuple(sorted(da[j] for j in range(n) if a[i]&(1<<j)))) for i in range(n)]
    sb=[(db[i],tuple(sorted(db[j] for j in range(n) if b[i]&(1<<j)))) for i in range(n)]
    if sorted(sa)!=sorted(sb): return
    domains=[[j for j in range(n) if sa[i]==sb[j] and (not fixed or i not in fixed or fixed[i]==j)] for i in range(n)]
    if any(not x for x in domains): return
    order=sorted(range(n),key=lambda i:(len(domains[i]),-da[i],i))
    p=[-1]*n
    def visit(t,used):
        if t==n:
            yield tuple(p); return
        i=order[t]
        for j in domains[i]:
            if used&(1<<j): continue
            if all(((a[i]>>order[k])&1)==((b[j]>>p[order[k]])&1) for k in range(t)):
                p[i]=j
                yield from visit(t+1,used|(1<<j))
        p[i]=-1
    yield from visit(0,0)

def inspect(a):
    n=len(a); d=[r.bit_count() for r in a]; W=[]; P=[]; cert=[]
    candidates=[(v,) for v in range(n)] + [(i,j) for i in range(n) for j in range(i+1,n) if a[i]&(1<<j)]
    for s in candidates:
        # These identities follow by counting cut edges, not by coverage.
        if len(s)==1 and 2*d[s[0]]!=n-1: continue
        if len(s)==2 and d[s[0]]+d[s[1]]!=n: continue
        b=switch(a,s); p=next(maps(b,a),None)
        if p is None: continue
        assert valid(b,a,p)
        cert.append({'vertices':list(s),'permutation':list(p)})
        (W if len(s)==1 else P).append(s[0] if len(s)==1 else s)
    U=sorted(set(range(n))-{v for s in P for v in s})
    return {'W':W,'P':[list(s) for s in P],'U':U,'covered':set(U)<=set(W),'switches':cert},len(candidates)

def family(f):
    m=len(f); a=[0]*(2*m+1)
    def edge(i,j): a[i]|=1<<j; a[j]|=1<<i
    for i in range(m):
        edge(0,1+i)
        for j in range(i):
            if f[i]&(1<<j):edge(1+i,1+j);edge(1+m+i,1+m+j)
        for j in range(m):
            if not f[i]&(1<<j):edge(1+i,1+m+j)
    return tuple(a)

def main():
    begin=time.monotonic(); report={'implementation':'independent bitset decoder, switch, static-domain exact bijection search; no original modules','catalogues':[],'essential':[],'family':[],'lemma_checks':0}
    expected_report=json.loads((ROOT/'data/independent_review.json').read_text())
    for n in range(1,10):
        path=graph_input(n) if n>=3 else None
        lines=path.open() if n>=3 else iter(['@'] if n==1 else ['A?','A_'])
        hist=Counter(); covered=[]; count=0; decisions=0; positives=0
        expected=json.loads((ROOT/'data'/f'covered_n{n}.json').read_text())
        old={r['graph6']:r for r in expected}
        for line in lines:
            code=line.strip(); a=decode(code);assert encode(a)==code and len(a)==n
            r,k=inspect(a); count+=1; decisions+=k;positives+=len(r['switches'])
            if n<=7:
                # Directly check all clauses of the transport lemma, even in uncovered graphs.
                for v in r['W']:
                    b=switch(a,[v]); rb,_=inspect(b)
                    pairs=[x for x in range(n) if x!=v and next(maps(switch(a,[v,x]),a),None) is not None]
                    assert set(rb['W'])=={v,*pairs}
                    for p in maps(b,a):
                        assert p[v] in r['W']
                        degP=sum(v in s for s in r['P'])
                        degW=sum(bool(a[p[v]]&(1<<x)) for x in r['W'])
                        assert degP==len(r['W'])-1-degW
                        report['lemma_checks']+=1
            if not r['covered']:continue
            hist[len(r['U'])]+=1
            r.update(graph6=code,n=n,degrees=[row.bit_count() for row in a]);covered.append(r)
            assert r==old[code], f'Covered record differs at order {n}: {code}'
            for s in old[code]['switches']:
                assert valid(switch(a,s['vertices']),a,s['permutation'])
            if r['U']:
                for v in r['U']:
                    mm=list(maps(switch(a,[v]),a))
                    assert mm and all(valid(switch(a,[v]),a,p) for p in mm)
                    detail={'graph6':code,'n':n,'v':v,'W':r['W'],'U':r['U'],'isomorphisms':len(mm),'fixing':sum(p[v]==v for p in mm),'permutation':list(mm[0])}
                    if n<=7:
                        brute=[p for p in permutations(range(n)) if valid(switch(a,[v]),a,p)]
                        assert set(mm)==set(brute)
                        detail['brute_permutations']=math.factorial(n)
                    report['essential'].append(detail)
            assert rss()<LIMIT
        if n>=3: lines.close()
        assert covered==expected, f'Covered catalogue differs at order {n}'
        row={'n':n,'input_classes':count,'switch_decisions':decisions,'positive_switches':positives,'covered':len(covered),'U_histogram':dict(sorted(hist.items()))}
        if n>=3:row['input_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        report['catalogues'].append(row)
        (ROOT/'data'/f'covered_n{n}.json').write_text(json.dumps(covered,indent=2)+'\n')
        print(json.dumps(row),flush=True)
    for m in range(2,6):
        pairs=list(combinations(range(m),2)); nonisolated=0
        for mask in range(1<<len(pairs)):
            f=[0]*m
            for k,(i,j) in enumerate(pairs):
                if mask&(1<<k):f[i]|=1<<j;f[j]|=1<<i
            a=family(f);r,_=inspect(a); isolated=[i for i in range(m) if not f[i]]
            w=[0]+[1+m+i for i in isolated]
            p=sorted([[0,1+i] for i in isolated]+[[1+i,1+m+j] for i in range(m) for j in range(m) if f[i]==f[j]])
            assert r['covered'] and r['W']==w and r['P']==p and r['U']==([] if isolated else [0])
            assert [row.bit_count() for row in a]==[m]+[m+1]*m+[m]*m
            tau=[0]+list(range(1+m,2*m+1))+list(range(1,1+m))
            assert valid(switch(a,[0]),a,tau)
            for s in p:
                perm=list(range(2*m+1));perm[s[0]],perm[s[1]]=perm[s[1]],perm[s[0]]
                assert valid(switch(a,s),a,perm)
            nonisolated+=not isolated
        row={'base_order':m,'labelled_bases':1<<len(pairs),'without_isolates':nonisolated}; report['family'].append(row); print(json.dumps(row),flush=True)
    # Compare all numerical results with the reviewed, repository-local report.
    assert json.loads(json.dumps(report))==expected_report
    assert rss()<LIMIT
    (ROOT/'data'/'independent_review.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS',time.monotonic()-begin,'seconds;',rss(),'bytes peak RSS',flush=True)
if __name__=='__main__':main()
