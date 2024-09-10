import enum
import inspect
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Union

from rich.console import Console
from rich.text import Text

console = Console()


class LogLevel(enum.Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    SUCCESS = 25
    FAILED = 35
    MESSAGE = 45


class PyLogger:
    _instance: Optional["PyLogger"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PyLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self, log_file_path: str, include_caller: bool = False):
        if not hasattr(self, "logger"):
            self.logger = logging.getLogger()
            self.logger.setLevel(logging.DEBUG)
            self._setup_handlers(log_file_path)
        self.include_caller = include_caller

    def _setup_handlers(self, log_file_path: str):
        # Setup file handler
        fh = logging.FileHandler(log_file_path, mode="w")
        fh.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%d-%m-%y %H:%M:%S",
        )
        fh.setFormatter(file_formatter)

        # Setup console handler
        sh = logging.StreamHandler()
        console_log_level = os.getenv("CONSOLE_LOG_LEVEL", "INFO")
        sh.setLevel(getattr(logging, console_log_level.upper(), logging.INFO))
        sh.setFormatter(
            ColorFormatter(
                "%(asctime)s | %(levelname)-8s | %(message)s",
                datefmt="%d-%m-%y %H:%M:%S",
            )
        )

        self.logger.addHandler(fh)
        self.logger.addHandler(sh)

    def log(
        self,
        level: LogLevel,
        msg: str,
        data: Optional[Union[Dict, List]] = None,
    ):
        if data and isinstance(data, (dict, list)):
            msg += f" -\n{json.dumps(data, indent=4)}"

        if self.include_caller:
            caller = self.get_caller_function()
            msg = f"{caller} | {msg}"

        timestamp = self.get_timestamp()

        if level in [LogLevel.SUCCESS, LogLevel.FAILED, LogLevel.MESSAGE]:
            self._set_color(level, timestamp, msg)
        else:
            self.logger.log(level.value, msg)

    # TODO Rename this here and in `log`
    def _set_color(self, level, timestamp, msg):
        color = (
            "green"
            if level == LogLevel.SUCCESS
            else "bold red"
            if level == LogLevel.FAILED
            else "cyan1"
        )

        log_text = Text()
        log_text.append(timestamp, style=color)
        log_text.append(f" | {level.name.ljust(8)} | ", style=color)
        log_text.append(msg, style=color)

        console.print(log_text)

    def debug(self, msg: str, data: Optional[Union[Dict, List]] = None):
        self.log(LogLevel.DEBUG, msg, data)

    def info(self, msg: str, data: Optional[Union[Dict, List]] = None):
        self.log(LogLevel.INFO, msg, data)

    def warning(self, msg: str, data: Optional[Union[Dict, List]] = None):
        self.log(LogLevel.WARNING, msg, data)

    def error(self, msg: str, data: Optional[Union[Dict, List]] = None):
        self.log(LogLevel.ERROR, msg, data)

    def critical(self, msg: str, data: Optional[Union[Dict, List]] = None):
        self.log(LogLevel.CRITICAL, msg, data)

    def success(self, msg: str):
        self.log(LogLevel.SUCCESS, msg)

    def failed(self, msg: str):
        self.log(LogLevel.FAILED, msg)

    def message(self, msg: str):
        self.log(LogLevel.MESSAGE, msg)

    def exception(self):
        console.print_exception(
            show_locals=False,
        )

    @staticmethod
    def get_timestamp() -> str:
        return datetime.now().strftime("%d-%m-%y %H:%M:%S")

    @staticmethod
    def get_caller_function() -> str:
        stack = inspect.stack()
        # Start from index 3 to skip the current method, log method, and the logger method
        for frame in stack[3:]:
            filename = frame.filename
            function = frame.function
            if not filename.endswith("pylogger.py"):
                caller_filename = os.path.join(
                    os.path.basename(os.path.dirname(filename)),
                    os.path.basename(filename),
                )
                return f"{caller_filename}::{function}"
        return "Unknown"


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[34m",  # CYAN
        logging.INFO: "\033[36m",  # WHITE
        logging.WARNING: "\033[33m",  # YELLOW
        logging.ERROR: "\033[31m",  # RED
        logging.CRITICAL: "\033[35m",  # MAGENTA
    }

    def format(self, record):
        color_code = self.COLORS.get(record.levelno, "\033[0m")
        message = super().format(record)
        return f"{color_code}{message}\033[0m"
