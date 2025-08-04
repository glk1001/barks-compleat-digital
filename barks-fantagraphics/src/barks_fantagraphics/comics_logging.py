from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler


class AnsiColor:
    """A helper class to encapsulate ANSI color codes for terminal output."""

    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

    RESET_SEQ = "\033[0m"
    BOLD_SEQ = "\033[1m"
    TOTAL_SEQ_LEN = len(BOLD_SEQ) + 4 + 2 + 1 + len(RESET_SEQ)

    @staticmethod
    def get_ansi_color_seq(color: int) -> str:
        return f"{AnsiColor.BOLD_SEQ}\033[1;{30 + color}m"


LOGGING_COLORS: dict[str, int] = {
    "DEBUG": AnsiColor.CYAN,
    "INFO": AnsiColor.GREEN,
    "WARNING": AnsiColor.YELLOW,
    "CRITICAL": AnsiColor.YELLOW,
    "ERROR": AnsiColor.RED,
    "FATAL": AnsiColor.RED,
}
MAX_LEVEL_LEN = 7  # don't count CRITICAL
MAX_LEVEL_LEN_WITH_COLOR = MAX_LEVEL_LEN + AnsiColor.TOTAL_SEQ_LEN
MAX_LOGGER_NAME_LEN = 4


def get_log_format(level_width: int) -> str:
    return f"%(asctime)s %(levelname)-{level_width}s: %(name)-{MAX_LOGGER_NAME_LEN}s: %(message)s"


PLAIN_FORMAT = get_log_format(MAX_LEVEL_LEN)
COLOR_FORMAT = get_log_format(MAX_LEVEL_LEN_WITH_COLOR)


class LogPlainFormatter(logging.Formatter):
    def __init__(self) -> None:
        super().__init__(PLAIN_FORMAT)


class LogColoredFormatter(logging.Formatter):
    """A log formatter that adds color to the output based on log level."""

    def __init__(self) -> None:
        super().__init__(COLOR_FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        # Create a copy of the record to avoid modifying the original.
        # This is safer and prevents side effects for other handlers.
        colored_rec = logging.makeLogRecord(record.__dict__)

        levelname = colored_rec.levelname
        if levelname in LOGGING_COLORS:
            color = LOGGING_COLORS[levelname]
            ansi_color_seq = AnsiColor.get_ansi_color_seq(color)
            colored_rec.levelname = f"{ansi_color_seq}{levelname}{AnsiColor.RESET_SEQ}"

        return super().format(colored_rec)


def setup_logging(
    log_level: str | int,
    logger_name: str = "",
    to_file_also: str = "",
) -> None:
    """Configure the root logger for the application.

    Args:
        log_level: The minimum logging level to process (e.g., logging.DEBUG).
        logger_name: An optional name to assign to the root logger.
        to_file_also: An optional path to a log file.

    """
    # Using force=True (Python 3.8+) removes any existing handlers from the root logger.
    # This ensures a clean setup every time this function is called.
    logging.basicConfig(level=log_level, force=True, handlers=[])

    if to_file_also:
        file_handler = RotatingFileHandler(to_file_also, maxBytes=5 * 1024 * 1024, backupCount=5)
        file_handler.setFormatter(LogPlainFormatter())
        logging.root.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(LogColoredFormatter())
    logging.root.addHandler(console_handler)

    if logger_name:
        logging.root.name = logger_name

    # TODO: Hack to stop third-party modules screwing with our logging.
    # Must be a better way.
    logging.root.setLevel(log_level)
