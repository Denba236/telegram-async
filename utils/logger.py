# telegram_async/utils/logger.py

import logging
import sys
from typing import Optional


# Color configuration for different logging levels
class ColoredFormatter(logging.Formatter):
    """Formatter with console colors"""

    grey = "\x1b[38;20m"
    blue = "\x1b[34;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey,
        logging.INFO: blue,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: bold_red
    }

    def format(self, record):
        log_color = self.FORMATS.get(record.levelno, self.grey)
        record.msg = f"{log_color}{record.msg}{self.reset}"
        return super().format(record)


def setup_logger(name: str = "telegram_async",
                 level: Optional[int] = None,
                 log_file: Optional[str] = None) -> logging.Logger:
    """
    Configures the logger for the library

    Args:
        name: Logger name
        level: Logging level (defaults to INFO)
        log_file: Path to log file (optional)

    Returns:
        Configured logger
    """
    if level is None:
        level = logging.INFO

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Console format (with colors)
    console_format = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # Optional file handler
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)

        # File format (without colors)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger


# Default logger for the library
logger = setup_logger()


def get_logger(name: str) -> logging.Logger:
    """
    Gets the logger for a specific module

    Args:
        name: Module name (usually __name__)

    Returns:
        Logger for the module
    """
    return logging.getLogger(f"telegram_async.{name}")


# Context logger class
class ContextLogger:
    """Logger with additional context"""

    def __init__(self, logger: logging.Logger, **context):
        self.logger = logger
        self.context = context

    def _log(self, level, msg, *args, **kwargs):
        if self.context:
            context_str = " ".join(f"[{k}={v}]" for k, v in self.context.items())
            msg = f"{context_str} {msg}"
        self.logger.log(level, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self._log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._log(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._log(logging.CRITICAL, msg, *args, **kwargs)


# Helper functions
def log_deprecation(message: str):
    """Logs a deprecation warning"""
    logger.warning(f"DEPRECATION WARNING: {message}")


def log_api_call(method: str, url: str, params: Optional[dict] = None):
    """Logs an API call"""
    if params:
        logger.debug(f"API {method} {url} - Params: {params}")
    else:
        logger.debug(f"API {method} {url}")


def log_api_response(method: str, url: str, status: int, time_ms: float):
    """Logs an API response"""
    logger.debug(f"API {method} {url} - Status: {status} - Time: {time_ms:.2f}ms")
