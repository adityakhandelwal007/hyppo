import pytest
import numpy as np
from numpy.testing import assert_almost_equal, assert_warns, assert_raises

from ...benchmarks.ksample_sim import linear_2samp
from .. import UnpairKSample
from ...independence import CannCorr, Dcorr


class TestUnpairKSamp:
    @pytest.mark.parametrize("n, obs_stat, obs_pvalue, indep_test", [
        (10, 0.0162, 0.693, CannCorr),
        (100, 8.24e-5, 0.981, CannCorr),
        (1000, 4.28e-7, 1.0, CannCorr),
        (10, 0.153, 0.091, Dcorr),
        (50, 0.0413, 0.819, Dcorr),
        (100, 0.0237, 0.296, Dcorr)
    ])
    def test_twosamp_linear_oned(self, n, obs_stat, obs_pvalue, indep_test):
        np.random.seed(123456789)
        x, y = linear_2samp(n, 1, noise=0)
        stat, pvalue = UnpairKSample(indep_test).test([x, y])

        assert_almost_equal(stat, obs_stat, decimal=1)
        assert_almost_equal(pvalue, obs_pvalue, decimal=1)


class TestUnpairKErrorWarn:
    """ Tests errors and warnings derived from MGC.
    """
    def test_error_notndarray(self):
        # raises error if x or y is not a ndarray
        x = np.arange(20)
        y = [5] * 20
        z = np.arange(5)
        assert_raises(ValueError, UnpairKSample(Dcorr).test, [x, y, z])

    def test_error_shape(self):
        # raises error if number of samples different (n)
        x = np.arange(100).reshape(25, 4)
        y = x.reshape(10, 10)
        z = x
        assert_raises(ValueError, UnpairKSample(Dcorr).test, [x, y, z])

    def test_error_lowsamples(self):
        # raises error if samples are low (< 3)
        x = np.arange(3)
        y = np.arange(3)
        assert_raises(ValueError, UnpairKSample(CannCorr).test, [x, y])

    def test_error_nans(self):
        # raises error if inputs contain NaNs
        x = np.arange(20, dtype=float)
        x[0] = np.nan
        assert_raises(ValueError, UnpairKSample(CannCorr).test, [x, x])

        y = np.arange(20)
        assert_raises(ValueError, UnpairKSample(CannCorr).test, [x, y])
