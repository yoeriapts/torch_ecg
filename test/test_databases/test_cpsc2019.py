"""
TestCPSC2019: accomplished
TestCPSC2019Dataset: accomplished

subsampling: accomplished
"""

import shutil
from copy import deepcopy
from pathlib import Path

import numpy as np
import pytest

from torch_ecg.databases import CPSC2019, DataBaseInfo
from torch_ecg.databases.cpsc_databases.cpsc2019 import compute_metrics
from torch_ecg.databases.datasets import CPSC2019Dataset, CPSC2019TrainCfg


###############################################################################
# set paths
_CWD = Path(__file__).absolute().parents[2] / "tmp" / "test-db" / "cpsc2019"
try:
    shutil.rmtree(_CWD)
except FileNotFoundError:
    pass
_CWD.mkdir(parents=True, exist_ok=True)
###############################################################################


reader = CPSC2019(_CWD)
reader.download()


class TestCPSC2019:
    def test_len(self):
        assert len(reader) == 2000

    def test_subsample(self):
        ss_ratio = 0.3
        reader_ss = CPSC2019(_CWD, subsample=ss_ratio, verbose=0)
        assert len(reader_ss) == pytest.approx(len(reader) * ss_ratio, abs=1)
        ss_ratio = 0.1 / len(reader)
        reader_ss = CPSC2019(_CWD, subsample=ss_ratio)
        assert len(reader_ss) == 1

        with pytest.raises(
            AssertionError, match="`subsample` must be in \\(0, 1\\], but got `.+`"
        ):
            CPSC2019(_CWD, subsample=0.0)
        with pytest.raises(
            AssertionError, match="`subsample` must be in \\(0, 1\\], but got `.+`"
        ):
            CPSC2019(_CWD, subsample=1.01)
        with pytest.raises(
            AssertionError, match="`subsample` must be in \\(0, 1\\], but got `.+`"
        ):
            CPSC2019(_CWD, subsample=-0.1)

    def test_load_data(self):
        data = reader.load_data(0)
        data_1 = reader.load_data(0, data_format="flat", units="μV")
        assert data.ndim == 2 and data.shape[0] == 1
        assert data_1.ndim == 1 and data_1.shape[0] == data.shape[1]
        assert np.allclose(data, data_1.reshape(1, -1) / 1000, atol=1e-2)
        data_1 = reader.load_data(0, data_format="flat", fs=2 * reader.fs)
        assert data_1.shape[0] == 2 * data.shape[1]

        with pytest.raises(ValueError, match="Invalid `data_format`: xxx"):
            reader.load_data(0, data_format="xxx")
        with pytest.raises(ValueError, match="Invalid `units`: kV"):
            reader.load_data(0, units="kV")

    def test_load_ann(self):
        ann = reader.load_ann(0)
        assert isinstance(ann, np.ndarray) and ann.ndim == 1

    def test_load_rpeaks(self):
        # alias of `load_ann`
        rpeaks = reader.load_rpeaks(0)
        assert np.allclose(rpeaks, reader.load_ann(0))

    def test_load_rpeak_indices(self):
        # alias of `load_ann`
        rpeaks = reader.load_rpeak_indices(0)
        assert np.allclose(rpeaks, reader.load_ann(0))

    def test_get_subject_id(self):
        assert isinstance(reader.get_subject_id(0), int)

    def test_meta_data(self):
        assert isinstance(reader.webpage, str) and len(reader.webpage) > 0
        assert reader.get_citation() is None  # printed
        assert isinstance(reader.database_info, DataBaseInfo)
        all_annotations = reader.all_annotations
        assert isinstance(all_annotations, list) and len(all_annotations) == len(reader)
        all_references = reader.all_references
        assert isinstance(all_references, list) and len(all_references) == len(reader)
        assert all_annotations == all_references

    def test_plot(self):
        reader.plot(0, ticks_granularity=2)
        data = reader.load_data(0, data_format="flat")
        reader.plot(0, data=data, ticks_granularity=1)
        data = reader.load_data(0, units="μV", data_format="flat")
        reader.plot(0, data=data, ticks_granularity=0)

    def test_compute_metrics(self):
        rpeaks_truths = np.array([500, 1000])
        rpeaks_preds = np.array([500, 700, 1000])
        QRS_acc = compute_metrics([rpeaks_truths], [rpeaks_preds], reader.fs, verbose=2)
        assert np.allclose(QRS_acc, 0.7)
        rpeaks_truths = reader.load_rpeaks(0)
        rpeaks_preds = reader.load_rpeaks(0)
        QRS_acc = compute_metrics([rpeaks_truths], [rpeaks_preds], reader.fs)
        assert np.allclose(QRS_acc, 1.0)


config = deepcopy(CPSC2019TrainCfg)
config.db_dir = _CWD
config.recover_length = False

with pytest.warns(
    RuntimeWarning, match="`db_dir` is specified in both config and reader_kwargs"
):
    ds = CPSC2019Dataset(config, training=False, lazy=False, db_dir=_CWD)


config_1 = deepcopy(config)
config_1.recover_length = True

ds_1 = CPSC2019Dataset(config_1, training=False, lazy=False)


class TestCPSC2019Dataset:
    def test_len(self):
        assert len(ds) == len(ds.records) > 0

    def test_getitem(self):
        assert config.n_leads == 1
        assert config.input_len == config_1.input_len > 0
        for i in range(len(ds)):
            data, bin_mask = ds[i]
            assert data.ndim == 2 and data.shape == (1, config.input_len)
            assert bin_mask.ndim == 2 and bin_mask.shape == (
                config.input_len // config.reduction,
                1,
            )
        for i in range(len(ds_1)):
            data, bin_mask = ds_1[i]
            assert data.ndim == 2 and data.shape == (1, config_1.input_len)
            assert bin_mask.ndim == 2 and bin_mask.shape == (config_1.input_len, 1)

    def test_properties(self):
        assert str(ds) == repr(ds)
