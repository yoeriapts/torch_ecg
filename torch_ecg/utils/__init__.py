"""
torch_ecg.utils
===============

This module contains a collection of utility functions and classes that are used
throughout the package.

.. contents:: torch_ecg.utils
    :depth: 2
    :local:
    :backlinks: top

.. currentmodule:: torch_ecg.utils

Neural network auxiliary functions and classes
----------------------------------------------
.. autosummary::
    :toctree: generated/
    :recursive:

    extend_predictions
    compute_output_shape
    compute_conv_output_shape
    compute_deconv_output_shape
    compute_maxpool_output_shape
    compute_avgpool_output_shape
    compute_sequential_output_shape
    compute_module_size
    default_collate_fn
    compute_receptive_field
    adjust_cnn_filter_lengths
    SizeMixin
    CkptMixin

Signal processing functions
---------------------------
.. autosummary::
    :toctree: generated/
    :recursive:

    smooth
    resample_irregular_timeseries
    detect_peaks
    remove_spikes_naive
    butter_bandpass_filter
    get_ampl
    normalize
    normalize_t
    resample_t

Data operations
---------------
.. autosummary::
    :toctree: generated/
    :recursive:

    get_mask
    class_weight_to_sample_weight
    ensure_lead_fmt
    ensure_siglen
    masks_to_waveforms
    mask_to_intervals
    uniform
    stratified_train_test_split
    cls_to_bin
    generate_weight_mask

Interval operations
-------------------
.. autosummary::
    :toctree: generated/
    :recursive:

    overlaps
    validate_interval
    in_interval
    in_generalized_interval
    intervals_union
    generalized_intervals_union
    intervals_intersection
    generalized_intervals_intersection
    generalized_interval_complement
    get_optimal_covering
    interval_len
    generalized_interval_len
    find_extrema
    is_intersect
    max_disjoint_covering

Metrics computations
--------------------
.. autosummary::
    :toctree: generated/
    :recursive:

    top_n_accuracy
    confusion_matrix
    ovr_confusion_matrix
    metrics_from_confusion_matrix
    compute_wave_delineation_metrics
    QRS_score

Decorators and Mixins
---------------------
.. autosummary::
    :toctree: generated/
    :recursive:

    add_docstring
    remove_parameters_returns_from_docstring
    default_class_repr
    ReprMixin
    CitationMixin
    get_kwargs
    get_required_args
    add_kwargs

Path operations
---------------
.. autosummary::
    :toctree: generated/
    :recursive:

    get_record_list_recursive3

String operations
-----------------
.. autosummary::
    :toctree: generated/
    :recursive:

    dict_to_str
    str2bool
    nildent
    get_date_str

Miscellaneous
-------------
.. autosummary::
    :toctree: generated/
    :recursive:

    init_logger
    list_sum
    dicts_equal
    MovingAverage
    Timer
    timeout

"""
from . import ecg_arrhythmia_knowledge as EAK
from .download import http_get
from .misc import (
    get_record_list_recursive3,
    dict_to_str,
    str2bool,
    init_logger,
    get_date_str,
    list_sum,
    dicts_equal,
    default_class_repr,
    ReprMixin,
    CitationMixin,
    MovingAverage,
    nildent,
    add_docstring,
    remove_parameters_returns_from_docstring,
    timeout,
    Timer,
    get_kwargs,
    get_required_args,
    add_kwargs,
)
from .utils_data import (
    get_mask,
    class_weight_to_sample_weight,
    ensure_lead_fmt,
    ensure_siglen,
    ECGWaveForm,
    ECGWaveFormNames,
    masks_to_waveforms,
    mask_to_intervals,
    uniform,
    stratified_train_test_split,
    cls_to_bin,
    generate_weight_mask,
)
from .utils_interval import (
    overlaps,
    validate_interval,
    in_interval,
    in_generalized_interval,
    intervals_union,
    generalized_intervals_union,
    intervals_intersection,
    generalized_intervals_intersection,
    generalized_interval_complement,
    get_optimal_covering,
    interval_len,
    generalized_interval_len,
    find_extrema,
    is_intersect,
    max_disjoint_covering,
)
from .utils_metrics import (
    top_n_accuracy,
    confusion_matrix,
    ovr_confusion_matrix,
    QRS_score,
    metrics_from_confusion_matrix,
    compute_wave_delineation_metrics,
)
from .utils_nn import (
    extend_predictions,
    compute_output_shape,
    compute_conv_output_shape,
    compute_deconv_output_shape,
    compute_maxpool_output_shape,
    compute_avgpool_output_shape,
    compute_sequential_output_shape,
    compute_module_size,
    default_collate_fn,
    compute_receptive_field,
    adjust_cnn_filter_lengths,
    SizeMixin,
    CkptMixin,
)
from .utils_signal import (
    smooth,
    resample_irregular_timeseries,
    detect_peaks,
    remove_spikes_naive,
    butter_bandpass_filter,
    get_ampl,
    normalize,
)
from .utils_signal_t import (
    normalize as normalize_t,
    resample as resample_t,
)


__all__ = [
    "EAK",
    "http_get",
    "get_record_list_recursive3",
    "dict_to_str",
    "str2bool",
    "init_logger",
    "get_date_str",
    "list_sum",
    "dicts_equal",
    "default_class_repr",
    "ReprMixin",
    "CitationMixin",
    "MovingAverage",
    "nildent",
    "add_docstring",
    "remove_parameters_returns_from_docstring",
    "timeout",
    "Timer",
    "get_kwargs",
    "get_required_args",
    "add_kwargs",
    "get_mask",
    "class_weight_to_sample_weight",
    "ensure_lead_fmt",
    "ensure_siglen",
    "ECGWaveForm",
    "ECGWaveFormNames",
    "masks_to_waveforms",
    "mask_to_intervals",
    "uniform",
    "stratified_train_test_split",
    "cls_to_bin",
    "generate_weight_mask",
    "overlaps",
    "validate_interval",
    "in_interval",
    "in_generalized_interval",
    "intervals_union",
    "generalized_intervals_union",
    "intervals_intersection",
    "generalized_intervals_intersection",
    "generalized_interval_complement",
    "get_optimal_covering",
    "interval_len",
    "generalized_interval_len",
    "find_extrema",
    "is_intersect",
    "max_disjoint_covering",
    "top_n_accuracy",
    "confusion_matrix",
    "ovr_confusion_matrix",
    "QRS_score",
    "metrics_from_confusion_matrix",
    "compute_wave_delineation_metrics",
    "extend_predictions",
    "compute_output_shape",
    "compute_conv_output_shape",
    "compute_deconv_output_shape",
    "compute_maxpool_output_shape",
    "compute_avgpool_output_shape",
    "compute_sequential_output_shape",
    "compute_module_size",
    "default_collate_fn",
    "compute_receptive_field",
    "adjust_cnn_filter_lengths",
    "SizeMixin",
    "CkptMixin",
    "smooth",
    "resample_irregular_timeseries",
    "detect_peaks",
    "remove_spikes_naive",
    "butter_bandpass_filter",
    "get_ampl",
    "normalize",
    "normalize_t",
    "resample_t",
]
