import numpy
from scipy.sparse import csc_matrix

from nextprod import nextprod

from . import _fglt_c


def fglt(n, d):

    return _fglt_c.count(n, d)