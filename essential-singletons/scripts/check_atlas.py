#!/usr/bin/env python3
"""Check atlas provenance and the stored essential-switch certificates."""
import gzip
import hashlib
import json
from independent_review import encode, decode, valid, switch, family, maps, inspect
from inputs import ROOT, download, graph_input


def main():
    raw = download('atlas-3.4.2.dat.gz').read_bytes()
    blocks = gzip.decompress(raw).decode().split('GRAPH ')[1:]
    by_n = {n: [] for n in range(8)}
    for block in blocks:
        lines = block.splitlines()
        n = int(lines[1].split()[1])
        a = [0] * n
        for line in lines[2:]:
            if not line.strip():
                continue
            i, j = map(int, line.split())
            a[i] |= 1 << j
            a[j] |= 1 << i
        by_n[n].append(encode(a))
    for n in range(3, 8):
        assert by_n[n] == graph_input(n).read_text().splitlines()
    nine = json.loads((ROOT / 'data/covered_n9.json').read_text())
    essential = [r for r in nine if r['U']]
    for r in essential:
        a = decode(r['graph6'])
        actual, _ = inspect(a)
        assert all(actual[key] == r[key] for key in actual)
        for s in r['switches']:
            assert valid(switch(a, s['vertices']), a, s['permutation'])
    for f, code in [((2, 5, 2), 'FBfnO'), ((6, 5, 3), 'F`urg')]:
        assert next(maps(family(f), decode(code)), None) is not None
    seven = json.loads((ROOT / 'data/covered_n7.json').read_text())
    assert {r['graph6'] for r in seven if r['U'] and set(r['degrees']) <= {3, 4}} == {'FBfnO', 'F`urg'}
    sources = json.loads((ROOT / 'data/sources.json').read_text())
    url = next(r['url'] for r in sources if r['name'] == 'atlas-3.4.2.dat.gz')
    result = {
        'atlas_source': url,
        'atlas_sha256': hashlib.sha256(raw).hexdigest(),
        'atlas_graph_count': len(blocks),
        'matches_supplied_orders': list(range(3, 8)),
        'order9_stored_essential_switch_lists_checked': len(essential),
        'order7_family_identifications_verified': True,
    }
    output = ROOT / 'data/atlas_and_certificates.json'
    assert result == json.loads(output.read_text())
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
