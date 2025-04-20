from typing import Literal

import numpy as np

import settings
from data_processing.utils import apply


@apply
def moving_average_filter(
    data: list[int | float],
    x_size: int,
    y_size: int,
    z_size: int,
    *,
    window_size: int = settings.MOVING_AVERAGE_DEFAULT_WINDOW_SIZE,
    axis: int = settings.MOVING_AVERAGE_DEFAULT_AXIS,
    mode: Literal["same", "valid", "full"] = settings.MOVING_AVERAGE_DEFAULT_MODE,
    window_type: Literal[
        "gaussian", "uniform"
    ] = settings.MOVING_AVERAGE_DEFAULT_WINDOW_TYPE,
    **kwargs,
):

    prepared_data = np.array(data)

    arr_3d = prepared_data.reshape((x_size, y_size, z_size))

    if window_type == "uniform":
        kernel = np.ones(window_size) / window_size
    elif window_type == "gaussian":
        kernel = np.exp(-np.linspace(-3, 3, window_size) ** 2 / 2)
        kernel /= kernel.sum()
    else:
        raise ValueError(f"unknown window type: {window_type}")

    smoothed = np.apply_along_axis(
        lambda m: np.convolve(m, kernel, mode=mode), axis=axis, arr=arr_3d
    )

    processed_data = smoothed.flatten().tolist()
    stats = {
        "mean": float(np.mean(processed_data)),
        "stddev": float(np.std(processed_data)),
        "min": float(np.min(processed_data)),
        "max": float(np.max(processed_data)),
    }

    return {
        "processed_data": processed_data,
        "stats": stats,
    }
