from pyfglt import fglt
import numpy as np


def test_example_function():
    assert np.array_equal(fglt(10, 3), np.zeros((10, 3)))
