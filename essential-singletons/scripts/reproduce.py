#!/usr/bin/env python3
"""Run the full numerical review sequentially in one Python process."""
import hashlib
import json

import check_atlas
import check_sources
import independent_review
from inputs import ROOT


def main():
    if not __debug__:
        raise RuntimeError('Run without -O: the numerical checks require assertions.')
    check_sources.main()
    independent_review.main()
    check_atlas.main()
    report = json.loads((ROOT / 'data/independent_review.json').read_text())
    rows = [row for row in report['catalogues'] if row['n'] >= 3]
    assert [row['covered'] for row in rows] == [1, 3, 3, 11, 10, 35, 33]
    assert [row['U_histogram'].get('1', 0) for row in rows] == [0, 0, 1, 0, 6, 0, 16]
    assert all(set(row['U_histogram']) <= {'0', '1'} for row in rows)
    # Order one is also an essential singleton; the note's table starts at three.
    essential = [r for r in report['essential'] if r['n'] >= 3]
    assert len(essential) == 23
    assert all(r['W'] == r['U'] == [r['v']] and r['fixing'] == r['isomorphisms'] for r in essential)
    final_path = ROOT / 'data/final_checks.json'
    final = json.loads(final_path.read_text())
    for name, expected in final['historical_note_review']['note_sha256'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected
    final['numerical_rerun'] = {
        'reviewed_catalogues_and_certificates_reproduced': True,
        'orders': list(range(3, 10)),
        'covered': [row['covered'] for row in rows],
        'exactly_one_essential_singleton': [row['U_histogram'].get('1', 0) for row in rows],
        'essential_cases_all_switching_isomorphisms_fix_vertex': len(essential),
        'transport_lemma_checks': report['lemma_checks'],
        'labelled_construction_bases_checked': sum(row['labelled_bases'] for row in report['family']),
    }
    artifacts = [ROOT / 'note.tex', ROOT / 'note.pdf', ROOT / 'README.md']
    artifacts += sorted((ROOT / 'scripts').glob('*.py'))
    artifacts += sorted(p for p in (ROOT / 'data').glob('*.json') if p != final_path)
    final['sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in artifacts}
    assert independent_review.rss() < independent_review.LIMIT
    final_path.write_text(json.dumps(final, indent=2) + '\n')
    print(f'PASS full numerical review; {independent_review.rss()} bytes peak RSS', flush=True)


if __name__ == '__main__':
    main()
