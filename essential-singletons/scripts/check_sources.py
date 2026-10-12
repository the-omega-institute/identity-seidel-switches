#!/usr/bin/env python3
"""Verify local catalogues and fetch pinned numerical inputs, never source PDFs."""
from inputs import download, graph_input


def main():
    for n in range(3, 10):
        path = graph_input(n)
        print(f'PASS order {n}: {path.name} SHA-256', flush=True)
    path = download('atlas-3.4.2.dat.gz')
    print(f'PASS atlas: {path.name} SHA-256', flush=True)


if __name__ == '__main__':
    main()
