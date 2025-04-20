import logging
from logging.handlers import RotatingFileHandler

import settings

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

console_handler = logging.StreamHandler()
console_handler.setLevel(settings.CONSOLE_LOG_LEVEL)
console_handler.setFormatter(formatter)

file_handler = RotatingFileHandler(
    filename=settings.LOG_FILE,
    maxBytes=1024 * 1024 * 512,  # 512 MB
    backupCount=5,
    encoding="utf-8",
)

file_handler.setLevel(settings.FILE_LOG_LEVEL)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
