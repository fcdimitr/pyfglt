import numpy
import scipy.sparse as sp
from scipy.sparse import csc_matrix, issparse

import networkx as nx
import numpy as np
from typeguard import typechecked
from typing import Union

from pyfglt import _fglt_c

import pandas as pd

COLUMNS = [
    "[0] vertex (==1)",
    "[1] degree",
    "[2] 2-path",
    "[3] bifork",
    "[4] 3-cycle",
    "[5] 3-path, end",
    "[6] 3-path, interior",
    "[7] claw, leaf",
    "[8] claw, root",
    "[9] paw, handle",
    "[10] paw, base",
    "[11] paw, center",
    "[12] 4-cycle",
    "[13] diamond, off-cord",
    "[14] diamond, on-cord",
    "[15] 4-clique",
]

@typechecked
def compute(A: Union[nx.Graph, csc_matrix]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute the counts fo the Fast Graphlet Transform.

    Args:
        A (Union[nx.Graph, csc_matrix]): The adjacency matrix of the graph.

    Accepts either an undirected, unweighted NetworkX graph or a CSC sparse matrix.
    If a NetworkX graph is provided, converts it to a CSC adjacency matrix.
    If a CSC matrix is provided, verifies that it is unweighted and symmetric.

    Returns:
        F (DataFrame): A dataframe with the counts of the graphlets.
    """

    # If input is a NetworkX graph
    if isinstance(A, nx.Graph):
        # Ensure it's undirected
        if A.is_directed():
            raise ValueError("Graph must be undirected.")
        
        # Convert to adjacency matrix in CSC format
        adj_matrix = nx.adjacency_matrix(A)
        csc_adj = adj_matrix.tocsc()

    # If input is already a CSC matrix
    elif issparse(A) and isinstance(A, csc_matrix):
        csc_adj = A  # Use directly

        # Ensure symmetry (A == A.T)
        if not (abs(csc_adj - csc_adj.T)).nnz == 0:
            raise ValueError("CSC matrix must be symmetric (undirected graph).")

        # Ensure unweighted (all elements are 0 or 1)
        if not np.all(np.isin(csc_adj.data, [0, 1])):
            raise ValueError("CSC matrix must be unweighted (contain only 0s and 1s).")
        
    else:
        raise TypeError("Input must be either a NetworkX undirected graph or a CSC matrix.")

    f, fn = _fglt_c.count(csc_adj)

    # cast f and fn to int64
    f = f.astype(numpy.int64)
    fn = fn.astype(numpy.int64)

    # transpose f and fn
    f = f.T
    fn = fn.T

    # transform to dataframe
    F  = pd.DataFrame(f, columns=COLUMNS)
    FN = pd.DataFrame(fn, columns=COLUMNS)

    # set index name to "Node id (0-based)"
    F.index.name = "Node id (0-based)"
    FN.index.name = "Node id (0-based)"

    return F, FN
