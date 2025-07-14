import logging
import sys

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# The background is set with 40 plus the number of the color, and the foreground with 30.
# These are the sequences need to get colored output.
RESET_SEQ = "\033[0m"
BOLD_SEQ = "\033[1m"


def get_color_seq(color: int) -> str:
    return f"\033[1;{30 + color}m"


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


LOGGING_COLORS = {
    "DEBUG": CYAN,
    "INFO": GREEN,
    "WARNING": YELLOW,
    "CRITICAL": YELLOW,
    "ERROR": RED,
    "FATAL": RED,
}

FORMAT = "%(asctime)s %(levelname)-18s: %(message)s"
COLOR_FORMAT = formatter_message(FORMAT, True)


class LogColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in LOGGING_COLORS:
            levelname_color = f"{get_color_seq(LOGGING_COLORS[levelname])}{levelname}{RESET_SEQ}"
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


def setup_logging(log_level) -> None:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(LogColoredFormatter(COLOR_FORMAT))
    logging.root.addHandler(handler)

    # TODO: Hack to stop third-party modules screwing with our logging.
    # Must be a better way.
    logging.root.setLevel(log_level)
