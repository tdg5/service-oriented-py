from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Generator, Generic, TypeVar

from service_oriented.application.config import BaseConfig


SomeConfig = TypeVar("SomeConfig", bound=BaseConfig)
SomeContainer = TypeVar("SomeContainer")


class AbstractCompositionRoot(Generic[SomeConfig, SomeContainer], ABC):
    def __init__(self, config: SomeConfig) -> None:
        self.config = config

    def run(self) -> None:
        with self.container() as container:
            self.run_with_container(container=container)

    @contextmanager
    @abstractmethod
    def container(self) -> Generator[SomeContainer, None, None]:
        pass  # pragma: no cover

    @abstractmethod
    def run_with_container(self, container: SomeContainer) -> None:
        pass  # pragma: no cover
