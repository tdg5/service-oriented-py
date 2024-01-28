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


class NoDefaultsApplication(BaseApplication):
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


def test_application_init_subclass() -> None:
    entry_points = {
        "other": EntryPointSpec(CallbackEntryPoint),
    }

    class InitSubclassApplication(BaseApplication, entry_points=entry_points):
        pass

    assert entry_points == InitSubclassApplication.default_entry_points


def test_application_init() -> None:
    class InitApplication(
        BaseApplication,
        entry_points={
            "default": EntryPointSpec(CallbackEntryPoint),
            "override": EntryPointSpec(CallbackEntryPoint),
        },
    ):
        pass

    config = Config(
        deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
        entry_point=TEST_ENTRY_POINT,
    )
    instance_entry_points = {
        "instance": EntryPointSpec(CallbackEntryPoint),
        "override": EntryPointSpec(CallbackEntryPoint),
    }
    application = InitApplication(
        config=config,
        entry_points=instance_entry_points,
    )
    assert config == application.config
    assert instance_entry_points["instance"] == application.entry_points["instance"]
    assert instance_entry_points["override"] == application.entry_points["override"]
    expected_default_entry_point = InitApplication.default_entry_points["default"]
    assert expected_default_entry_point == application.entry_points["default"]


def test_application_run() -> None:
    on_run_called = False

    def on_run_callback() -> None:
        nonlocal on_run_called
        on_run_called = True

    config = Config(
        deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
        entry_point=TEST_ENTRY_POINT,
    )

    application = NoDefaultsApplication(
        config=config,
        entry_points={
            TEST_ENTRY_POINT: EntryPointSpec(
                CallbackEntryPoint,
                on_run_callback=on_run_callback,
            ),
        },
    )

    application.run()
    assert on_run_called


def test_application_run_raises_for_unknown_entry_point() -> None:
    config = Config(
        deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
        entry_point="other",
    )

    application = NoDefaultsApplication(
        config=config,
        entry_points={
            TEST_ENTRY_POINT: EntryPointSpec(CallbackEntryPoint),
        },
    )

    with pytest.raises(RuntimeError) as exinfo:
        application.run()

    assert RuntimeError == exinfo.type
    exception_message = str(exinfo.value)
    assert "No mapping found for entry point named 'other'" == exception_message
