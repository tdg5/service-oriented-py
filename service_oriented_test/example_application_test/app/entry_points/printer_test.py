import logging
from contextlib import contextmanager
from logging import Logger
from logging import config as logging_config
from typing import Generator

from pytest_mock import MockerFixture
from rodi import Container

from service_oriented.services.logger_service import (
    AbstractLoggerService,
    LoggerService,
)
from service_oriented_test.example_application.app.entry_points.printer import (
    PrinterEntryPoint,
)
from service_oriented_test.example_application_test import factories


class DefaultLoggerService(AbstractLoggerService):
    def get_logger(self, name: str) -> Logger:
        # This keeps the type checker happy, but really, a test should patch
        # this function on an instance for optimal control.
        return logging.getLogger(name)


class PrinterEntryPointWithCustomContainer(PrinterEntryPoint):
    @contextmanager
    def container(self) -> Generator[Container, None, None]:
        try:
            container = Container()
            container.add_instance(DefaultLoggerService(), AbstractLoggerService)
            yield container
        finally:
            pass


def test_container_includes_a_logger_service(mocker: MockerFixture) -> None:
    config = factories.config()
    printer_entry_point = PrinterEntryPoint(config=config)
    spy = mocker.spy(logging_config, "dictConfig")
    with printer_entry_point.container() as container:
        assert 1 == spy.call_count
        provider = container.build_provider()
        assert isinstance(provider.get(AbstractLoggerService), LoggerService)


def test_run_logs_hello_world(mocker: MockerFixture) -> None:
    config = factories.config()
    mock_logger = mocker.MagicMock()
    mocker.patch.object(DefaultLoggerService, "get_logger", return_value=mock_logger)
    printer_entry_point = PrinterEntryPointWithCustomContainer(config=config)
    printer_entry_point.run()
    mock_logger.info.assert_called_with("hello world")
