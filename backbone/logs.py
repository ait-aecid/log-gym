from datetime import datetime
import logging

from typing import Callable

store_logs = True
__do_timestamp = True
path_logs = "logs.log"
module = "Standard"
history = []


def as_test():
    global __do_timestamp
    global module
    __do_timestamp = False
    module = "Test"


def update_configuration():
    if store_logs:
        logging.basicConfig(
            filename=path_logs, 
            encoding="utf-8",
            filemode='w',
            level=logging.DEBUG
        )


def __log_format(level: str, msg: str) -> str:
    time = datetime.now().strftime("[%Y-%m-%d/%H:%M:%S]")
    timestamp = f"{time}" if __do_timestamp else ""
    return f"{timestamp} {level}:{module} {msg}"


def __apply_log(msg: str, level: str, func: Callable[[str], None]) -> None:
    if msg is None:
        return None

    msg = __log_format(level, msg)
    history.append(msg)
    if store_logs:
        func(msg)


def debug(msg: str) -> None:
    __apply_log(msg=msg, level="DEBUG", func=logging.debug)


def info(msg: str) -> None:
    __apply_log(msg=msg, level="INFO", func=logging.info)


def warning(msg: str) -> None:
    __apply_log(msg=msg, level="WARNING", func=logging.warning)


def error(msg: str) -> None:
    __apply_log(msg=msg, level="ERROR", func=logging.error)

def trace(msg: str) -> None:
    __apply_log(msg=msg, level="TRACE", func=logging.info)

