from contextlib import contextmanager
from typing import Generator

from rodi import Container

from service_oriented.application.abstract_composition_root import (
    AbstractCompositionRoot,
)
from service_oriented.services.logger_service import (
    LoggerService,
    LoggerServiceWithYamlLoggingConfig,
)
from service_oriented_test.example_application.app.config import Config


class PrinterEntryPoint(AbstractCompositionRoot[Config, Container]):
    def __init__(self, config: Config) -> None:
        self.config = config

    @contextmanager
    def container(self) -> Generator[Container, None, None]:
        try:
            container = Container()
            container.add_instance(
                LoggerServiceWithYamlLoggingConfig(
                    yaml_path=self.config.logging_config_yaml_path,
                ),
                LoggerService,
            )
            yield container
        finally:
            pass

    def run_with_container(self, container: Container) -> None:
        services = container.build_provider()
        logger_service = services.get(LoggerService)
        logger = logger_service.get_logger(__name__)
        logger.info("hello world")
