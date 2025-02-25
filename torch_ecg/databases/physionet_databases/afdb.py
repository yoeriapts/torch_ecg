# -*- coding: utf-8 -*-

import math
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

import numpy as np
import wfdb

from ...cfg import CFG
from ...utils.misc import add_docstring, get_record_list_recursive
from ...utils.utils_interval import generalized_intervals_intersection
from ..base import DEFAULT_FIG_SIZE_PER_SEC, PhysioNetDataBase, DataBaseInfo


__all__ = [
    "AFDB",
]


_AFDB_INFO = DataBaseInfo(
    title="""
    MIT-BIH Atrial Fibrillation Database
    """,
    about="""
    1. contains 25 long-term (each 10 hours) ECG recordings of human subjects with atrial fibrillation (mostly paroxysmal)
    2. 23 records out of 25 include the two ECG signals, the left 2 records 00735 and 03665 are represented only by the rhythm (.atr) and unaudited beat (.qrs) annotation files
    3. signals are sampled at 250 samples per second with 12-bit resolution over a range of ±10 millivolts, with a typical recording bandwidth of approximately 0.1 Hz to 40 Hz
    4. 4 classes of rhythms are annotated:

        - AFIB:  atrial fibrillation
        - AFL:   atrial flutter
        - J:     AV junctional rhythm
        - N:     all other rhythms

    5. rhythm annotations almost all start with "(N", except for 4 which start with '(AFIB', which are all within 1 second (250 samples)
    6. Webpage of the database on PhysioNet [1]_. Paper describing the database [2]_.
    """,
    note="""
    1. beat annotation files (.qrs files) were prepared using an automated detector and have NOT been corrected manually
    2. for some records, manually corrected beat annotation files (.qrsc files) are available
    3. one should never use wfdb.rdann with arguments `sampfrom`, since one has to know the `aux_note` (with values in ["(N", "(J", "(AFL", "(AFIB"]) before the index at `sampfrom`
    """,
    usage=[
        "Atrial fibrillation (AF) detection",
    ],
    references=[
        "https://physionet.org/content/afdb/",
        "Moody GB, Mark RG. A new method for detecting atrial fibrillation using R-R intervals. Computers in Cardiology. 10:227-230 (1983).",
    ],
    doi=[
        "10.13026/C2MW2D",
    ],
)


@add_docstring(_AFDB_INFO.format_database_docstring(), mode="prepend")
class AFDB(PhysioNetDataBase):
    """
    Parameters
    ----------
    db_dir : str or pathlib.Path, optional
        Storage path of the database.
        If not specified, data will be fetched from Physionet.
    working_dir : str, optional
        Working directory, to store intermediate files and log files.
    verbose : int, default 1
        Level of logging verbosity.
    kwargs : dict, optional
        Auxilliary key word arguments.

    """

    __name__ = "AFDB"

    def __init__(
        self,
        db_dir: Optional[Union[str, Path]] = None,
        working_dir: Optional[str] = None,
        verbose: int = 1,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            db_name="afdb",
            db_dir=db_dir,
            working_dir=working_dir,
            verbose=verbose,
            **kwargs,
        )
        self.fs = 250
        self.data_ext = "dat"
        self.ann_ext = "atr"
        self.auto_beat_ann_ext = "qrs"
        self.manual_beat_ann_ext = "qrsc"

        self.all_leads = [
            "ECG1",
            "ECG2",
        ]

        self.special_records = ["00735", "03665"]
        self.qrsc_records = None
        self._ls_rec()

        self.class_map = CFG(AFIB=1, AFL=2, J=3, N=0)  # an extra isoelectric
        self.palette = kwargs.get("palette", None)
        if self.palette is None:
            self.palette = CFG(
                AFIB="blue",
                AFL="red",
                J="yellow",
                # N="green",
                qrs="green",
            )

    def _ls_rec(self, local: bool = True) -> None:
        """
        Find all records (relative path without file extension),
        and save into `self._all_records` for further use.

        Parameters
        ----------
        local : bool, default True
            If True, read from local storage,
            prior to using :func:`wfdb.get_record_list`.

        """
        super()._ls_rec(local=local)
        self._all_records = [
            rec for rec in self._all_records if rec not in self.special_records
        ]
        self.qrsc_records = get_record_list_recursive(
            self.db_dir, self.manual_beat_ann_ext, relative=False
        )
        self.qrsc_records = [Path(rec).stem for rec in self.qrsc_records]

    def load_ann(
        self,
        rec: Union[str, int],
        sampfrom: Optional[int] = None,
        sampto: Optional[int] = None,
        ann_format: str = "interval",
        keep_original: bool = False,
    ) -> Union[Dict[str, list], np.ndarray]:
        """Load annotations (header) from the .hea files.

        Parameters
        ----------
        rec : str or int
            Record name or index of the record in :attr:`all_records`.
        sampfrom : int, optional
            Start index of the annotations to be loaded.
        sampto: int, optional
            End index of the annotations to be loaded.
        ann_format : {"interval", "mask"}
            Format of returned annotation,
            by default "interval", case insensitive.
        keep_original : bool, default False
            If True, when `ann_format` is "interval",
            intervals (in the form [a,b]) will keep the same with the annotation file,
            otherwise subtract `sampfrom` if specified.

        Returns
        -------
        ann : dict or numpy.ndarray
            The annotations in the format of intervals, or in the format of masks.

        """
        fp = str(self.get_absolute_path(rec))
        wfdb_ann = wfdb.rdann(fp, extension=self.ann_ext)
        header = wfdb.rdheader(fp)
        sig_len = header.sig_len
        sf = sampfrom or 0
        st = sampto or sig_len
        assert st > sf, "`sampto` should be greater than `sampfrom`!"

        ann = CFG({k: [] for k in self.class_map.keys()})
        critical_points = wfdb_ann.sample.tolist() + [sig_len]
        aux_note = wfdb_ann.aux_note
        if aux_note[0] == "(N":
            # ref. the doc string of the class
            critical_points[0] = 0
        else:
            critical_points.insert(0, 0)
            aux_note.insert(0, "(N")

        for idx, rhythm in enumerate(aux_note):
            ann[rhythm.replace("(", "")].append(
                [critical_points[idx], critical_points[idx + 1]]
            )
        ann = CFG(
            {
                k: generalized_intervals_intersection(l_itv, [[sf, st]])
                for k, l_itv in ann.items()
            }
        )

        if ann_format.lower() == "mask":
            tmp = deepcopy(ann)
            ann = np.full(shape=(st - sf,), fill_value=self.class_map.N, dtype=int)
            for rhythm, l_itv in tmp.items():
                for itv in l_itv:
                    ann[itv[0] - sf : itv[1] - sf] = self.class_map[rhythm]
        elif not keep_original:
            for k, l_itv in ann.items():
                ann[k] = [[itv[0] - sf, itv[1] - sf] for itv in l_itv]

        return ann

    def load_beat_ann(
        self,
        rec: Union[str, int],
        sampfrom: Optional[int] = None,
        sampto: Optional[int] = None,
        use_manual: bool = True,
        keep_original: bool = False,
    ) -> np.ndarray:
        """Load beat annotations from corresponding annotation files.

        Parameters
        ----------
        rec : str or int
            Record name or index of the record in :attr:`all_records`.
        sampfrom : int, optional
            Start index of the annotations to be loaded.
        sampto : int, optional
            End index of the annotations to be loaded.
        use_manual : bool, default True
            If True, use manually annotated beat annotations (qrs),
            instead of those generated by algorithms.
        keep_original : bool, default False
            If True, indices will keep the same with the annotation file,
            otherwise subtract `sampfrom` if specified.

        Returns
        -------
        ann : numpy.ndarray
            Locations (indices) of the qrs complexes.

        """
        if isinstance(rec, int):
            rec = self[rec]
        fp = str(self.get_absolute_path(rec))
        if use_manual and rec in self.qrsc_records:
            ext = self.manual_beat_ann_ext
        else:
            ext = self.auto_beat_ann_ext
        ann = wfdb.rdann(
            fp,
            extension=ext,
            sampfrom=sampfrom or 0,
            sampto=sampto,
        )
        ann = ann.sample
        if not keep_original and sampfrom is not None:
            ann -= sampfrom
        return ann

    @add_docstring(load_beat_ann.__doc__)
    def load_rpeak_indices(
        self,
        rec: Union[str, int],
        sampfrom: Optional[int] = None,
        sampto: Optional[int] = None,
        use_manual: bool = True,
        keep_original: bool = False,
    ) -> np.ndarray:
        """
        alias of `self.load_beat_ann`
        """
        return self.load_beat_ann(rec, sampfrom, sampto, use_manual, keep_original)

    def plot(
        self,
        rec: Union[str, int],
        data: Optional[np.ndarray] = None,
        ann: Optional[Dict[str, np.ndarray]] = None,
        rpeak_inds: Optional[Union[Sequence[int], np.ndarray]] = None,
        ticks_granularity: int = 0,
        leads: Optional[Union[str, int, List[str], List[int]]] = None,
        sampfrom: Optional[int] = None,
        sampto: Optional[int] = None,
        same_range: bool = False,
        **kwargs: Any,
    ) -> None:
        """
        Plot the signals of a record or external signals (units in μV),
        with metadata (fs, labels, tranche, etc.),
        possibly also along with wave delineations.

        Parameters
        ----------
        rec : str or int
            Record name or index of the record in :attr:`all_records`.
        data : numpy.ndarray, optional
            (2-lead) ECG signal to plot,
            should be of the format "channel_first", and compatible with `leads`.
            If given, data of `rec` will not be used,
            which is useful when plotting filtered data.
        ann : dict, optional
            Annotations for `data`, covering those from annotation files,
            in the form of ``{"AFIB":l_itv, "AFL":l_itv, "J":l_itv, "N":l_itv}``,
            where ``l_itv`` in the form of ``[[a, b], ...]``.
            Ignored if `data` is None.
        rpeak_inds : array_like, optional
            Indices of R peaks, covering those from annotation files.
            If `data` is None, then indices should be the absolute indices in the record.
        ticks_granularity : int, default 0
            Granularity to plot axis ticks, the higher the more ticks.
            0 (no ticks) --> 1 (major ticks) --> 2 (major + minor ticks).
        leads : str or int or List[str] or List[int], optional
            The leads to plot.
        sampfrom : int, optional
            Start index of the data to plot.
        sampto : int, optional
            End index of the data to plot.
        same_range : bool, default False
            If True, forces all leads to have the same y range.
        kwargs : dict, optional
            Keyword arguments for :func:`matplotlib.pyplot.plot`, etc.

        """
        if isinstance(rec, int):
            rec = self[rec]
        if "plt" not in dir():
            import matplotlib.pyplot as plt

            plt.MultipleLocator.MAXTICKS = 3000
        if leads is None or leads == "all":
            _leads = self.all_leads
        elif isinstance(leads, str):
            _leads = [leads]
        elif isinstance(leads, int):
            _leads = [self.all_leads[leads]]
        else:
            _leads = leads
        assert all([ld in self.all_leads for ld in _leads]) or set(_leads) <= {0, 1}

        try:
            lead_indices = [self.all_leads.index(ld) for ld in _leads]
        except ValueError:
            lead_indices = _leads
        if data is None:
            _data = self.load_data(
                rec,
                leads=_leads,
                sampfrom=sampfrom,
                sampto=sampto,
                data_format="channel_first",
                units="μV",
            )
        else:
            units = self._auto_infer_units(data)
            self.logger.info(f"input data is auto detected to have units in `{units}`")
            if units.lower() == "mv":
                _data = 1000 * data
            else:
                _data = data
            _leads = [f"ECG_{idx}" for idx in range(_data.shape[0])]
        if ann is None and data is None:
            _ann = self.load_ann(
                rec,
                sampfrom=sampfrom,
                sampto=sampto,
                ann_format="interval",
                keep_original=False,
            )
        else:
            _ann = ann or CFG({k: [] for k in self.class_map.keys()})
        # indices to time
        _ann = {
            k: [[itv[0] / self.fs, itv[1] / self.fs] for itv in l_itv]
            for k, l_itv in _ann.items()
        }
        if rpeak_inds is None and data is None:
            _rpeak = self.load_rpeak_indices(
                rec,
                sampfrom=sampfrom,
                sampto=sampto,
                use_manual=True,
                keep_original=False,
            )
            _rpeak = _rpeak / self.fs  # indices to time
        else:
            _rpeak = np.array(rpeak_inds or []) / self.fs  # indices to time

        ann_plot_alpha = 0.2
        rpeaks_plot_alpha = 0.8

        nb_leads = len(_leads)

        line_len = self.fs * 25  # 25 seconds
        nb_lines = math.ceil(_data.shape[1] / line_len)

        for seg_idx in range(nb_lines):
            seg_data = _data[..., seg_idx * line_len : (seg_idx + 1) * line_len]
            secs = (np.arange(seg_data.shape[1]) + seg_idx * line_len) / self.fs
            seg_ann = {
                k: generalized_intervals_intersection(l_itv, [[secs[0], secs[-1]]])
                for k, l_itv in _ann.items()
            }
            seg_rpeaks = _rpeak[np.where((_rpeak >= secs[0]) & (_rpeak < secs[-1]))[0]]
            fig_sz_w = int(
                round(DEFAULT_FIG_SIZE_PER_SEC * seg_data.shape[1] / self.fs)
            )
            if same_range:
                y_ranges = (
                    np.ones((seg_data.shape[0],)) * np.max(np.abs(seg_data)) + 100
                )
            else:
                y_ranges = np.max(np.abs(seg_data), axis=1) + 100
            fig_sz_h = 6 * y_ranges / 1500
            fig, axes = plt.subplots(
                nb_leads, 1, sharex=True, figsize=(fig_sz_w, np.sum(fig_sz_h))
            )
            if nb_leads == 1:
                axes = [axes]
            for idx in range(nb_leads):
                axes[idx].plot(
                    secs, seg_data[idx], color="black", label=f"lead - {_leads[idx]}"
                )
                axes[idx].axhline(y=0, linestyle="-", linewidth="1.0", color="red")
                # NOTE that `Locator` has default `MAXTICKS` equal to 1000
                if ticks_granularity >= 1:
                    axes[idx].xaxis.set_major_locator(plt.MultipleLocator(0.2))
                    axes[idx].yaxis.set_major_locator(plt.MultipleLocator(500))
                    axes[idx].grid(
                        which="major", linestyle="-", linewidth="0.5", color="red"
                    )
                if ticks_granularity >= 2:
                    axes[idx].xaxis.set_minor_locator(plt.MultipleLocator(0.04))
                    axes[idx].yaxis.set_minor_locator(plt.MultipleLocator(100))
                    axes[idx].grid(
                        which="minor", linestyle=":", linewidth="0.5", color="black"
                    )
                for k, l_itv in seg_ann.items():
                    if k == "N":
                        continue
                    for itv in l_itv:
                        axes[idx].axvspan(
                            itv[0],
                            itv[1],
                            color=self.palette[k],
                            alpha=ann_plot_alpha,
                            label=k,
                        )
                for ri in seg_rpeaks:
                    axes[idx].axvspan(
                        ri - 0.01,
                        ri + 0.01,
                        color=self.palette["qrs"],
                        alpha=rpeaks_plot_alpha,
                    )
                    axes[idx].axvspan(
                        ri - 0.075,
                        ri + 0.075,
                        color=self.palette["qrs"],
                        alpha=ann_plot_alpha,
                    )
                axes[idx].legend(loc="upper left")
                axes[idx].set_xlim(secs[0], secs[-1])
                axes[idx].set_ylim(-y_ranges[idx], y_ranges[idx])
                axes[idx].set_xlabel("Time [s]")
                axes[idx].set_ylabel("Voltage [μV]")
            plt.subplots_adjust(hspace=0.2)
            plt.show()

    @property
    def database_info(self) -> DataBaseInfo:
        return _AFDB_INFO
