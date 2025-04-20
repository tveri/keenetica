import numpy as np
import pytest

from data_processing import median_filter, moving_average_filter


# Фикстуры для тестовых данных
@pytest.fixture
def sample_3d_data_ones():
    data = np.ones((2, 2, 2)).flatten().tolist()
    return {
        "data": data,
        "x_size": 2,
        "y_size": 2,
        "z_size": 2,
    }


@pytest.fixture
def sample_3d_data_outlier():
    data = np.ones((3, 3, 1))
    data[1, 1, 0] = 100
    return {
        "data": data.flatten().tolist(),
        "x_size": 3,
        "y_size": 3,
        "z_size": 1,
    }


def test_median_filter_default_apply(sample_3d_data_ones):
    result = median_filter(**sample_3d_data_ones)
    assert result["processed_data"] == sample_3d_data_ones["data"]
    assert np.isclose(result["stats"]["mean"], 1.0, rtol=1e-09, atol=1e-09)
    assert np.isclose(result["stats"]["stddev"], 0.0, rtol=1e-09, atol=1e-09)


def test_median_filter_apply_false(sample_3d_data_ones):
    result = median_filter(**sample_3d_data_ones, apply=False)
    assert result["processed_data"] == sample_3d_data_ones["data"]
    assert result["stats"] is None


def test_median_filter_outlier_removal(sample_3d_data_outlier):
    result = median_filter(
        **sample_3d_data_outlier, window_shape=(3, 3), pad_mode="edge"
    )
    processed = np.array(result["processed_data"]).reshape(3, 3, 1)
    assert np.isclose(processed[1, 1, 0], 1.0, rtol=1e-09, atol=1e-09)


def test_median_filter_padding_modes():
    data = np.zeros((3, 3, 1))
    data[1, 1, 0] = 1
    result = median_filter(
        data=data.flatten().tolist(),
        x_size=3,
        y_size=3,
        z_size=1,
        window_shape=(3, 3),
        pad_mode="constant",
    )
    processed = np.array(result["processed_data"])
    assert np.count_nonzero(processed) == 0
