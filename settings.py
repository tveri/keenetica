import logging
from os import getenv
from pathlib import Path
from typing import Final, Literal

from dotenv import load_dotenv

load_dotenv()


BASE_PATH = Path(__file__).parent

HOST: Final[str] = getenv("HOST", "127.0.0.1")
PORT: Final[int] = int(getenv("PORT", 8000))


#
# logging
#

LOG_FILE: Final[Path] = BASE_PATH / "keenetica.log"
CONSOLE_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.DEBUG

#
# filters settings
#

FILTERS_PARAMS_PATH = BASE_PATH / "params.tmp"
DELETE_FILTERS_PARAMS_ON_EXIT: Final[bool] = True

# moving average filter settings
MOVING_AVERAGE_DEFAULT_APPLY: Final[bool] = False
MOVING_AVERAGE_DEFAULT_WINDOW_SIZE: Final[int] = 3
MOVING_AVERAGE_DEFAULT_AXIS: Final[int] = 2
MOVING_AVERAGE_DEFAULT_MODE: Final[Literal["same", "valid", "full"]] = "same"
MOVING_AVERAGE_DEFAULT_WINDOW_TYPE: Final[Literal["gaussian", "uniform"]] = "uniform"

# median filter settings
MEDIAN_FILTER_DEFAULT_APPLY: Final[bool] = True
MEDIAN_FILTER_DEFAULT_WINDOW_SHAPE: tuple[int, int] = (3, 3)
MEDIAN_FILTER_DEFAULT_PAD_MODE: Literal["edge", "constant", "reflect"] = "edge"
