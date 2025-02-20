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
def compute(A: Union[nx.Graph, csc_matrix], raw: bool = False) -> Union[pd.DataFrame, tuple[pd.DataFrame, pd.DataFrame]]:
    """Compute the counts fo the Fast Graphlet Transform.

    Args:
        A (Union[nx.Graph, csc_matrix]): Either the graph as a `networkx.Graph` object 
                                         or the adjacency matrix of the graph in `scipy.sparse.csc_matrix` format.
        raw (bool): If True, return both the raw and the net counts of the graphlets. 
                    If False, then return only the normalized counts. 
                    Defaults to False.

    Accepts either an undirected, unweighted NetworkX graph or a CSC sparse matrix.
    If a NetworkX graph is provided, converts it to a CSC adjacency matrix.
    If a CSC matrix is provided, verifies that it is unweighted and symmetric.

    Returns:
        F (DataFrame): A dataframe with the net counts of the graphlets.
        F_raw (DataFrame): A dataframe with the raw counts of the graphlets (if raw=True).
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

    if raw:
        return FN, F
    else:
        return FN

@typechecked
def compute_rgf_distance(df_g1:pd.DataFrame, df_g2:pd.DataFrame) -> float:
    """Relative Graphlet Frequency (RGF)

    Args:
        df_g1 (pd.DataFrame): Orbit counts for Graph 1 (rows=vertices, columns=orbits).
        df_g2 (pd.DataFrame): Orbit counts for Graph 2 (rows=vertices, columns=orbits).

    Compute the Relative Graphlet Frequency (RGF) distance between two graphs
    represented by DataFrames of orbit counts.
        
    Returns:
        d (float): The RGF distance between the two graphs.
    """

    # Sum of orbit counts across all vertices for each orbit
    orbit_sums_g1 = df_g1.sum(axis=0)  # Series of length = number_of_orbits
    orbit_sums_g2 = df_g2.sum(axis=0)

    # Compute total counts
    total_g1 = orbit_sums_g1.sum()
    total_g2 = orbit_sums_g2.sum()

    # Relative frequencies for each orbit
    rel_freq_g1 = orbit_sums_g1 / total_g1 if total_g1 != 0 else orbit_sums_g1 * 0
    rel_freq_g2 = orbit_sums_g2 / total_g2 if total_g2 != 0 else orbit_sums_g2 * 0

    # RGF distance = sum of absolute differences
    rgf_distance = np.sum(np.abs(rel_freq_g1 - rel_freq_g2))
    return rgf_distance


@typechecked
def compute_graphlet_correlation_matrix(df_g:pd.DataFrame, method='spearman'):
    """
    Compute the Graphlet Correlation Matrix (GCM) for a single graph.

    Args:
        df_g (pd.DataFrame): Orbit counts for a graph (rows=vertices, columns=orbits).
        method (str) Correlation method. Can be 'pearson', 'spearman', or 'kendall'.

    Returns:
        C (pd.DataFrame): Correlation matrix of shape (n_orbits, n_orbits).
    """
    return df_g.iloc[:,1:].corr(method=method)


@typechecked
def gcm_distance(gcm1:pd.DataFrame, gcm2:pd.DataFrame):
    """
    Compute a simple distance between two correlation matrices.
    For instance, the sum of absolute differences (L1 distance).

    Args:
        gcm1 (pd.DataFrame): GCM of the first graph
        gcm2 (pd.DataFrame): GCM of the second graph

    Returns:
        d (float): A distance measure between the two GCMs.
    """
    diff = gcm1.values - gcm2.values
    return np.sum(np.abs(diff))


@typechecked
def compute_gdd_agreement(df_g1: pd.DataFrame, df_g2:pd.DataFrame, bins=None):
    """
    Compute Graphlet Degree Distribution (GDD) agreement between two graphs.

    Args:
        df_g1 (pd.DataFrame): Orbit counts for Graph 1 (rows=vertices, columns=orbits).
        df_g2 (pd.DataFrame): Orbit counts for Graph 2 (rows=vertices, columns=orbits).
        bins (Union[int, sequence]): Bins for histogram. If None, will try an automatic approach.

    Returns:
        s (float): The GDD agreement in [0, 1].
    """
    n_orbits = df_g1.shape[1]
    # We assume df_g1 and df_g2 have the same shape: #orbits = n_orbits

    # We can find a reasonable range for all orbit degrees combined
    combined_max = max(df_g1.values.max(), df_g2.values.max())
    if bins is None:
        # We'll bin from 0 up to the max count + 1
        bins = np.arange(0, combined_max + 2) - 0.5  # so that each integer is its own bin

    overlaps = []
    
    for orbit_col in df_g1.columns:
        # Distribution for Graph 1, orbit_col
        hist_g1, _ = np.histogram(df_g1[orbit_col], bins=bins, density=True)
        # Distribution for Graph 2, orbit_col
        hist_g2, _ = np.histogram(df_g2[orbit_col], bins=bins, density=True)
        
        # Overlap for this orbit
        overlap = np.sum(np.minimum(hist_g1, hist_g2))
        overlaps.append(overlap)
    
    # Average overlap across orbits
    gdd_agreement = np.mean(overlaps)
    return gdd_agreement