import pytest

from pyfglt.fglt import compute
from pyfglt.fglt import COLUMNS

import numpy as np

from scipy.io import mmread
from scipy.sparse import csc_matrix
import networkx as nx

import pandas as pd
from pandas.testing import assert_frame_equal

@pytest.mark.parametrize('mtxname', ['s6', 's12'])
def test_sample_graphs(mtxname):
    with open(f'subprojects/fglt-2.0.0/testdata/{mtxname}.mtx', 'r', encoding='utf-8') as mm_file:
        P = csc_matrix(mmread(mm_file))

    fn = compute(P)

    fn_gold = pd.read_csv(f'subprojects/fglt-2.0.0/testdata/{mtxname}_freq_net_gold.csv', index_col = 0)

    assert_frame_equal(fn, fn_gold, check_dtype=False)

@pytest.mark.parametrize('n', [8, 13, 17])
def test_star_graph(n):
    g = nx.star_graph(n)
    fn = compute(g)

    # create a dataframe using COLUMNS as columns from a numpy array
    # of length n+1 by 16; fill with zeros
    fn_gold = pd.DataFrame(np.zeros((n+1, 16), dtype=int), columns=COLUMNS, index=range(n+1))
    fn_gold.index.name = "Node id (0-based)"

    # manually set the values for the star graph
    fn_gold.loc[:, '[0] vertex (==1)'] = 1
    
    fn_gold.loc[1:, '[1] degree'] = 1
    fn_gold.loc[0, '[1] degree'] = n
    
    fn_gold.loc[1:, '[2] 2-path'] = n-1
    
    fn_gold.loc[0, '[3] bifork'] = ( n * (n-1) ) // 2
    
    fn_gold.loc[1:, '[7] claw, leaf'] = ( (n-1) * (n-2) ) // 2
    
    fn_gold.loc[0, '[8] claw, root'] = ( (n) * (n-1) * (n-2) ) // 6

    # assert that the computed values match the manually set values
    assert_frame_equal(fn, fn_gold, check_dtype=False)
