from typing import Literal

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

import settings
from data_processing.utils import apply


@apply
def median_filter(
    data: list[int | float],
    x_size: int,
    y_size: int,
    z_size: int,
    *,
    window_shape: tuple[int, int] = settings.MEDIAN_FILTER_DEFAULT_WINDOW_SHAPE,
    pad_mode: Literal[
        "edge", "constant", "reflect"
    ] = settings.MEDIAN_FILTER_DEFAULT_PAD_MODE,
    **kwargs,
):
    prepared_data = np.array(data)

    data_3d = prepared_data.reshape((x_size, y_size, z_size))
    processed_3d = np.empty_like(data_3d)

    h_pad = window_shape[0] // 2
    w_pad = window_shape[1] // 2

    for z in range(z_size):
        layer = data_3d[:, :, z]

        padded_layer = np.pad(
            layer,
            pad_width=((h_pad, h_pad), (w_pad, w_pad)),
            mode=pad_mode,
        )

        windows = sliding_window_view(padded_layer, window_shape)
        filtered_layer = np.median(windows, axis=(-2, -1))
        processed_3d[:, :, z] = filtered_layer

    stats = {
        "mean": float(np.mean(processed_3d)),
        "stddev": float(np.std(processed_3d)),
        "min": float(np.min(processed_3d)),
        "max": float(np.max(processed_3d)),
    }

    processed_data = processed_3d.ravel().tolist()

    return {
        "processed_data": processed_data,
        "stats": stats,
    }
