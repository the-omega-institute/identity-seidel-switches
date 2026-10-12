"""Repository-local inputs and checksum-pinned downloads (standard library only)."""
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
CACHE = ROOT / '.cache'


def verify(path, expected):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != expected:
        raise ValueError(f'SHA-256 mismatch for {path.name}: {digest} != {expected}')
    return path


def download(name):
    """Use only manifest URLs; verify both cached and newly downloaded bytes."""
    records = json.loads((ROOT / 'data/sources.json').read_text())
    record = next(r for r in records if r['name'] == name)
    CACHE.mkdir(exist_ok=True)
    path = CACHE / name
    if not path.exists():
        request = urllib.request.Request(record['url'], headers={
            'User-Agent': 'identity-seidel-switches reproducibility check'})
        # Both required inputs are below 3 MB. Bound unexpected responses too.
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read(10_000_001)
        if len(raw) > 10_000_000:
            raise ValueError(f'Download exceeds 10 MB limit: {name}')
        if hashlib.sha256(raw).hexdigest() != record['sha256']:
            raise ValueError(f'SHA-256 mismatch for downloaded {name}')
        temporary = path.with_suffix(path.suffix + '.part')
        temporary.write_bytes(raw)
        temporary.replace(path)
    return verify(path, record['sha256'])


def graph_input(n):
    if n == 9:
        return download('graph9.g6')
    if not 3 <= n <= 8:
        raise ValueError(f'No catalogue input for order {n}')
    name = f'all_n{n}.g6'
    provenance = json.loads((REPO / 'data/provenance.json').read_text())
    return verify(REPO / 'data' / name, provenance['inputs'][name]['sha256'])
