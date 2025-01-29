# pyFGLT: Fast Graphlet Transform in Python


We provide pyFGLT, a wrapper to a C/C++ multi-threaded library, for [Fast
Graphlet Transform](https://ieeexplore.ieee.org/abstract/document/9286205) of
large, sparse, undirected networks/graphs. Graphlets are used as encoding
elements to capture topological connectivity quantitatively and transform a
graph $G=(V,E)$ into a $|V| \times K$ array of graphlet frequencies at all
vertices. The $K$-element vector at each vertex represents the frequencies of
induced subgraphs, incident at the vertex, of the graphlet patterns. The
transformed data array serves multiple types of network analysis: statistical
or/and topological measures, comparison, classification, modeling, feature
embedding and dynamic variation, among others. The library pyFGLT is
distinguished in the following key aspects. (1) It is based on the fast, sparse
and exact transform formulas which are of the lowest time and space complexities
among known algorithms, and, at the same time, in ready form for globally
streamlined computation in matrix-vector operations. (2) It leverages prevalent
multi-core processors, with multi-threaded programming in Cilk, and uses sparse
graph computation techniques to deliver high-performance network analysis to
individual laptops or desktop computers.

A graph element, a.k.a. [graphlet](https://en.wikipedia.org/wiki/Graphlets), is
a connected template graph with a small number of nodes with or without a
designated incidence orbit (shown in red below). The graphlet patterns of up to
four nodes are shown below.

![](https://raw.githubusercontent.com/fcdimitr/fglt/master/figs/graphlet-dictionary.png)

## Installation

Install this library using `pip`:
```bash
pip install pyfglt
```

## Usage

See the examples under:

- [Getting started](tutorial/01-getting-started.md)
- [Advanced usage](tutorial/02-graphlet-based-network-properties.md)

for a quick start and advanced usage of the library.

## Citation

If you use this package, please cite this paper:

```bibtex
@article{fglt,
    author = {Floros, Dimitris and Pitsianis, Nikos and Sun, Xiaobai},
    journal = {IEEE HPEC},
    pages = {1--8},
    title = {{Fast graphlet transform of sparse graphs}},
    year = {2020}
}
```

