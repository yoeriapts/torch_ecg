"""
"""

from random import randint
from typing import Any, NoReturn, Sequence, Union, Optional
from numbers import Real

import numpy as np
import torch
from torch import Tensor

from .base import Augmenter


__all__ = ["RandomMasking",]


class RandomMasking(Augmenter):
    """
    Randomly mask ECGs with a probability.
    """
    __name__ = "RandomMasking"

    def __init__(self,
                 fs:int,
                 prob:Union[Sequence[Real],Real]=[0.3,0.15],
                 mask_value:Real=0.0,
                 mask_width:Sequence[Real]=[0.08,0.18],
                 inplace:bool=True,
                 **kwargs: Any) -> None:
        """ finished, checked,

        Parameters
        ----------
        fs: int,
            sampling frequency of the ECGs to be augmented
        prob: sequence of real numbers or real number, default [0.3,0.15],
            probabilities of masking ECG signals,
            the first probality is for the batch dimension,
            the second probability is for the lead dimension.
            note that 0.15 is approximately the proportion of QRS complexes in ECGs.
        mask_value: real number, default 0.0,
            value to mask with.
        mask_width: sequence of real numbers, default [0.08,0.18],
            width range of the masking window, with units in seconds
        inplace: bool, default True,
            whether to mask inplace or not
        kwargs: Keyword arguments.
        """
        super().__init__(**kwargs)
        self.fs = fs
        self.prob = prob
        if isinstance(self.prob, Real):
            self.prob = np.array([self.prob, self.prob])
        else:
            self.prob = np.array(self.prob)
        assert (self.prob >= 0).all() and (self.prob <= 1).all(), \
            "Probability must be between 0 and 1"
        self.mask_value = mask_value
        self.mask_width = (np.array(mask_width) * self.fs).round().astype(int)
        self.inplace = inplace

    def generate(self,
                 sig:Tensor,
                 label:Optional[Tensor]=None,
                 critical_points:Optional[Sequence[Sequence[int]]]=None) -> Tensor:
        """ finished, checked,

        Parameters
        ----------
        sig: Tensor,
            the ECGs to be augmented, of shape (batch, lead, siglen)
        label: Tensor,
            label tensor of the ECGs, not used

        Returns
        -------
        sig: Tensor,
            the augmented ECGs, of shape (batch, lead, siglen)
        """
        batch, lead, siglen = sig.shape
        if not self.inplace:
            sig = sig.clone()
        if self.prob[0] == 0:
            return sig
        sig_mask_prob = self.prob[1] / self.mask_width[1]
        sig_mask_scale_ratio = min(self.prob[1]/4, 0.1) / self.mask_width[1]
        mask = torch.full_like(sig, 1, dtype=sig.dtype, device=sig.device)
        for batch_idx in self.get_indices(prob=self.prob[0], pop_size=batch):
            if critical_points is not None:
                indices = self.get_indices(prob=self.prob[1], pop_size=len(critical_points[batch_idx]))
                indices = np.arange(siglen)[indices]
            else:
                indices = np.array(self.get_indices(
                    prob=sig_mask_prob,
                    pop_size=siglen-self.mask_width[1],
                    scale_ratio=sig_mask_scale_ratio,
                ))
                indices += self.mask_width[1]//2
            for j in indices:
                masked_radius = randint(self.mask_width[0], self.mask_width[1]) // 2
                mask[batch_idx, :, j-masked_radius:j+masked_radius] = self.mask_value
            print(f"batch_idx = {batch_idx}, len(indices) = {len(indices)}")
        sig = sig.mul_(mask)
        return sig

    def __call__(self,
                 sig:Tensor,
                 label:Optional[Tensor]=None,
                 critical_points:Optional[Sequence[Sequence[int]]]=None) -> Tensor:
        """
        alias of `self.generate`
        """
        return self.generate(sig, label, critical_points)
