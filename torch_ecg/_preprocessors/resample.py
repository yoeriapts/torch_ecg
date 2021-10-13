"""
resample the signal into fixed sampling frequency or length
"""

from typing import NoReturn, Optional, Any
from numbers import Real

import numpy as np
import scipy.signal as SS

from .base import PreProcessor


__all__ = ["Resample",]


class Resample(PreProcessor):
    """
    """
    __name__ = "Resample"

    def __init__(self, fs:Optional[int]=None, siglen:Optional[int]=None, **kwargs:Any) -> NoReturn:
        """ finished, NOT checked,

        Parameters
        ----------
        fs: int, optional,
            sampling frequency of the resampled ECG
        siglen: int, optional,
            number of samples in the resampled ECG

        NOTE that one and only one of `fs` and `siglen` should be set
        """
        self.fs = fs
        self.siglen = siglen
        assert sum([bool(self.fs), bool(self.siglen)]) == 1, \
            "one and only one of `fs` and `siglen` should be set"

    def apply(self, sig:np.ndarray, fs:Real) -> np.ndarray:
        """ finished, NOT checked,

        apply the preprocessor to `sig`

        Parameters
        ----------
        sig: ndarray,
            the ECG signal, can be
            1d array, which is a single-lead ECG
            2d array, which is a multi-lead ECG of "lead_first" format
            3d array, which is a tensor of several ECGs, of shape (batch, lead, siglen)
        fs: real number,
            sampling frequency of the ECG signal

        Returns
        -------
        rsmp_sig: ndarray,
            the resampled ECG signal
        """
        self.__check_sig(sig)
        if self.fs is not None:
            rsmp_sig = SS.resample_poly(sig, up=self.fs, down=fs, axis=-1)
        else:  # self.siglen is not None
            rsmp_sig = SS.resample(sig, num=self.siglen, axis=-1)
        return rsmp_sig