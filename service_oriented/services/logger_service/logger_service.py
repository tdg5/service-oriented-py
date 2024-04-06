from logging import Logger
from typing import Protocol


class LoggerService(Protocol):
    def get_logger(self, name: str) -> Logger:
        """Return a logger instance with the given name"""
