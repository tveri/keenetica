# Тесты для moving_average_filter
import numpy as np
import pytest

from data_processing import moving_average_filter


def test_moving_average_default_apply():
    data = np.ones(8).tolist()
    result = moving_average_filter(
        data=data, x_size=2, y_size=2, z_size=2, window_size=1
    )
    assert result["processed_data"] == data
    assert np.isclose(result["stats"]["mean"], 1.0, rtol=1e-09, atol=1e-09)


def test_moving_average_apply_false():
    data = [1.0, 2.0, 3.0, 4.0]
    result = moving_average_filter(data=data, x_size=2, y_size=2, z_size=1, apply=False)
    assert result["processed_data"] == data
    assert result["stats"] is None


@pytest.mark.parametrize(
    "window_type,expected",
    [
        ("uniform", [0.5, 2.0]),
        ("gaussian", [0.5, 2.0]),
    ],
)
def test_moving_average_types(window_type, expected):
    data = [1.0, 3.0]
    result = moving_average_filter(
        data=data,
        x_size=2,
        y_size=1,
        z_size=1,
        window_size=2,
        window_type=window_type,
        axis=0,
        mode="same",
    )
    assert np.allclose(result["processed_data"], expected, atol=0.1)


def test_moving_average_invalid_window_type():
    with pytest.raises(ValueError):
        moving_average_filter(
            data=[1.0] * 8, x_size=2, y_size=2, z_size=2, window_type="invalid"
        )


@pytest.mark.parametrize(
    "axis,mode,expected_size", [(0, "valid", 12), (1, "same", 24), (2, "full", 48)]
)
def test_moving_average_modes(axis, mode, expected_size):
    data = np.arange(24).tolist()  # 4x3x2
    result = moving_average_filter(
        data=data,
        x_size=4,
        y_size=3,
        z_size=2,
        window_size=3,
        window_type="uniform",
        axis=axis,
        mode=mode,
    )
    assert len(result["processed_data"]) == expected_size
