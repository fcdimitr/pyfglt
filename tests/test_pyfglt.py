import pytest

from pyfglt.fglt import compute
import numpy as np

from scipy.io import mmread
from scipy.sparse import csc_matrix

import pandas as pd
from pandas.testing import assert_frame_equal

@pytest.mark.parametrize('mtxname', ['s6', 's12'])
def test_example_function(mtxname):
    with open(f'subprojects/fglt-2.0.0/testdata/{mtxname}.mtx', 'r', encoding='utf-8') as mm_file:
        P = csc_matrix(mmread(mm_file))

    f, fn = compute(P)

    fn_gold = pd.read_csv(f'subprojects/fglt-2.0.0/testdata/{mtxname}_freq_net_gold.csv', index_col = 0)

    assert_frame_equal(fn, fn_gold, check_dtype=False)