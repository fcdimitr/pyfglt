import numpy
import scipy.sparse as sp
from scipy.sparse import csc_matrix

from nextprod import nextprod

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

def compute(A: csc_matrix) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute the counts fo the Fast Graphlet Transform.

    Args:
        A (csc_matrix): The adjacency matrix of the graph.

    Returns:
        F (DataFrame): A dataframe with the counts of the graphlets.
    """

    # create a random symmetric sparse matrix

    f, fn = _fglt_c.count(A)

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
