"""
"""

from copy import deepcopy

import torch

from torch_ecg.models.cnn.densenet import DenseNet
from torch_ecg.model_configs.cnn.densenet import (
    densenet_vanilla,
    densenet_leadwise,
)


IN_CHANNELS = 12


@torch.no_grad()
def test_densenet():
    inp = torch.randn(2, IN_CHANNELS, 2000)

    for item in [densenet_vanilla, densenet_leadwise]:
        config = deepcopy(item)
        config.dropout = 0.1
        model = DenseNet(in_channels=IN_CHANNELS, **config)
        model = model.eval()
        out = model(inp)
        assert out.shape == model.compute_output_shape(
            seq_len=inp.shape[-1], batch_size=inp.shape[0]
        )
        assert model.in_channels == IN_CHANNELS
        assert isinstance(model.doi, list)

    densenet_config = deepcopy(densenet_vanilla)
    densenet_config.block.building_block = "bottleneck"
    densenet_config.dropout = {"type": "1d", "p": 0.1}
    model = DenseNet(in_channels=IN_CHANNELS, **densenet_config)
    model = model.eval()
    out = model(inp)
    assert out.shape == model.compute_output_shape(
        seq_len=inp.shape[-1], batch_size=inp.shape[0]
    )

    densenet_config = deepcopy(densenet_leadwise)
    densenet_config.block.building_block = "bottleneck"
    densenet_config.dropout = {"type": None, "p": 0.1}
    model = DenseNet(in_channels=IN_CHANNELS, **densenet_config)
    model = model.eval()
    out = model(inp)
    assert out.shape == model.compute_output_shape(
        seq_len=inp.shape[-1], batch_size=inp.shape[0]
    )
