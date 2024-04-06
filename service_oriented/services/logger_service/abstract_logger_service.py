from abc import ABC, abstractmethod
from logging import Logger


class AbstractLoggerService(ABC):
    @abstractmethod
    def get_logger(self, name: str) -> Logger:
        pass
