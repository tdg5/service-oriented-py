from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Generator, Generic, TypeVar

from rodi import Container, Services

from service_oriented.application.config import BaseConfig


SomeConfig = TypeVar("SomeConfig", bound=BaseConfig)
SomeContainer = TypeVar("SomeContainer", bound=Container)


class AbstractCompositionRoot(Generic[SomeConfig, SomeContainer], ABC):
    def __init__(self, config: SomeConfig) -> None:
        self.config = config

    def run(self) -> None:
        with self.container() as container:
            services = container.build_provider()
            self.run_with_services(services=services)

    @contextmanager
    @abstractmethod
    def container(self) -> Generator[SomeContainer, None, None]:
        pass

    @abstractmethod
    def run_with_services(self, services: Services) -> None:
        pass
