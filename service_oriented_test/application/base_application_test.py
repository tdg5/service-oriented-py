from typing import Callable

import pytest

from service_oriented.application.base_application import BaseApplication
from service_oriented.application.config import BaseConfig
from service_oriented.application.entry_point_spec import EntryPointSpec
from service_oriented_test.test_helpers import (
    TEST_DEPLOYMENT_ENVIRONMENT,
    TEST_ENTRY_POINT,
)


class Config(
    BaseConfig,
    env_nested_delimiter="__",
    env_prefix="base_application_test_",
):
    pass


class CallbackEntryPoint:
    def __init__(
        self,
        config: Config,
        on_run_callback: Callable[[], None],
    ) -> None:
        self.config = config
        self.on_run_callback = on_run_callback

    def run(self) -> None:
        self.on_run_callback()


class Application(BaseApplication[Config]):
    pass


def test_application_init() -> None:
    config = Config(
        deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
        entry_point=TEST_ENTRY_POINT,
    )
    entry_points = {
        "other": EntryPointSpec(CallbackEntryPoint),
    }
    application = Application(
        config=config,
        entry_points=entry_points,
    )
    assert config == application.config
    assert entry_points == application.entry_points


def test_application_run() -> None:
    on_run_called = False

    def on_run_callback() -> None:
        nonlocal on_run_called
        on_run_called = True

    config = Config(
        deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
        entry_point=TEST_ENTRY_POINT,
    )
    entry_points = {
        TEST_ENTRY_POINT: EntryPointSpec(
            CallbackEntryPoint,
            on_run_callback=on_run_callback,
        ),
    }
    application = Application(
        config=config,
        entry_points=entry_points,
    )

    application.run()
    assert on_run_called


def test_application_run_raises_for_unknown_entry_point() -> None:
    config = Config(
        deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
        entry_point="other",
    )
    entry_points = {
        TEST_ENTRY_POINT: EntryPointSpec(CallbackEntryPoint),
    }
    application = Application(
        config=config,
        entry_points=entry_points,
    )

    with pytest.raises(RuntimeError) as exinfo:
        application.run()

    assert RuntimeError == exinfo.type
    exception_message = str(exinfo.value)
    assert "No mapping found for entry point named 'other'" == exception_message
