import pickle

import settings
from data_processing import median_filter, moving_average_filter
from logger import logger


def read_filters_params() -> dict:
    try:
        return pickle.load(open(settings.FILTERS_PARAMS_PATH, "rb"))
    except Exception:
        return {
            "median_filter": {},
            "moving_average": {},
        }


def handler(conn, request):
    filters_params = read_filters_params()

    x = request.get("x")
    y = request.get("y")
    z = request.get("z")

    data = request.get("data")
    stats = None

    result = median_filter(
        data,
        x,
        y,
        z,
        **filters_params["median_filter"],
    )

    data = result.get("processed_data")
    stats = new_stats if (new_stats := result.get("stats")) is not None else stats

    result = moving_average_filter(
        data,
        x,
        y,
        z,
        **filters_params["moving_average"],
    )

    data = result.get("processed_data")
    stats = new_stats if (new_stats := result.get("stats")) is not None else stats

    return {
        "processed_data": data,
        "stats": stats,
    }
