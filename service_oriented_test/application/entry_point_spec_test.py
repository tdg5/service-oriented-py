from typing import cast

from service_oriented.application.config import BaseConfig
from service_oriented.application.entry_point_spec import EntryPointSpec
from service_oriented_test.test_helpers import (
    TEST_DEPLOYMENT_ENVIRONMENT,
    TEST_ENTRY_POINT,
)


class Config(BaseConfig, env_nested_delimiter="__", env_prefix="entry_point_spec_test"):
    pass


class DummyEntryPoint:
    def __init__(self, config: Config, arg_1: str, arg_2: str) -> None:
        self.config = config
        self.arg_1 = arg_1
        self.arg_2 = arg_2

    def run(self) -> None:
        pass


def test_init() -> None:
    entry_point_class = DummyEntryPoint
    arg_1 = "arg_1"
    arg_2 = "arg_2"
    entry_point_spec = EntryPointSpec(entry_point_class, arg_1, arg_2=arg_2)
    assert entry_point_class == entry_point_spec.cls
    assert (arg_1,) == entry_point_spec.args
    assert {"arg_2": arg_2} == entry_point_spec.kwargs


def test_build() -> None:
    entry_point_class = DummyEntryPoint
    arg_1 = "arg_1"
    arg_2 = "arg_2"
    entry_point_spec = EntryPointSpec(entry_point_class, arg_1, arg_2=arg_2)
    config = Config(
        deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
        entry_point=TEST_ENTRY_POINT,
    )
    entry_point = cast(DummyEntryPoint, entry_point_spec.build(config))
    assert config == entry_point.config
    assert arg_1 == entry_point.arg_1
    assert arg_2 == entry_point.arg_2


def test_repr() -> None:
    entry_point_class = DummyEntryPoint
    arg_1 = "arg_1"
    arg_2 = "arg_2"
    entry_point_spec = EntryPointSpec(entry_point_class, arg_1, arg_2=arg_2)
    expected_repr = "EntryPointSpec(DummyEntryPoint, 'arg_1', arg_2='arg_2')"
    assert expected_repr == repr(entry_point_spec)
