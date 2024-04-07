from contextlib import contextmanager
from typing import Generator

from pytest_mock import MockerFixture

from service_oriented.application import AbstractCompositionRoot
from service_oriented.application.config import BaseConfig
from service_oriented_test.fixtures import TEST_DEPLOYMENT_ENVIRONMENT, TEST_ENTRY_POINT


class FakeConfig(
    BaseConfig,
    env_nested_delimiter="__",
    env_prefix="fake_config_",
):
    pass


class FakeContainer:
    pass


class ExampleCompositionRoot(AbstractCompositionRoot[FakeConfig, FakeContainer]):
    def __init__(self, config: FakeConfig, container: FakeContainer) -> None:
        super().__init__(config)
        self._container = container

    @contextmanager
    def container(self) -> Generator[FakeContainer, None, None]:
        try:
            yield self._container
        finally:
            pass

    def run_with_container(self, container: FakeContainer) -> None:
        pass


def test_run_creates_a_container_and_calls_run_container_with_it(
    mocker: MockerFixture,
) -> None:
    config = FakeConfig(
        deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
        entry_point=TEST_ENTRY_POINT,
    )
    container = FakeContainer()
    instance = ExampleCompositionRoot(config=config, container=container)
    run_with_container_mock = mocker.patch.object(instance, "run_with_container")
    instance.run()
    run_with_container_mock.assert_called_with(container=container)
