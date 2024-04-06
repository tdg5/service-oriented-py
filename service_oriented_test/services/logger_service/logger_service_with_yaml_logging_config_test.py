from logging import config as logging_config
from tempfile import NamedTemporaryFile
from uuid import uuid4

import pytest
from pytest_mock import MockerFixture

from service_oriented.services.logger_service.logger_service_with_yaml_logging_config import (  # noqa: E501
    LoggerServiceWithYamlLoggingConfig,
)


def test_logging_should_not_be_configured_given_a_non_existent_file(
    mocker: MockerFixture,
) -> None:
    spy = mocker.spy(logging_config, "dictConfig")
    LoggerServiceWithYamlLoggingConfig(yaml_path=f"/{uuid4()}/{uuid4()}/{uuid4()}")
    assert 0 == spy.call_count


def test_logging_should_be_configured_by_valid_yaml(
    mocker: MockerFixture,
) -> None:
    with NamedTemporaryFile(mode="w") as temp_file:
        temp_file.file.write("version: 1")
        temp_file.seek(0)
        spy = mocker.spy(logging_config, "dictConfig")
        LoggerServiceWithYamlLoggingConfig(yaml_path=temp_file.name)
        assert 1 == spy.call_count
        spy.assert_called_once_with({"version": 1})


def test_raises_if_config_file_is_invalid(
    mocker: MockerFixture,
) -> None:
    with NamedTemporaryFile(mode="w") as temp_file:
        temp_file.file.write("not_version: 1")
        temp_file.seek(0)
        with pytest.raises(ValueError) as exinfo:
            LoggerServiceWithYamlLoggingConfig(yaml_path=temp_file.name)
        assert ValueError == exinfo.type
        assert "dictionary doesn't specify a version" in str(exinfo.value)


def test_raises_if_config_file_does_not_deserialize_to_dict(
    mocker: MockerFixture,
) -> None:
    with NamedTemporaryFile(mode="w") as temp_file:
        temp_file.file.write("- version: 1")
        temp_file.seek(0)
        with pytest.raises(ValueError) as exinfo:
            LoggerServiceWithYamlLoggingConfig(yaml_path=temp_file.name)
        assert ValueError == exinfo.type
        assert "Expected logging config dict, received" in str(exinfo.value)
