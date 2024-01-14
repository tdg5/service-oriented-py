import pytest
from pydantic import ValidationError
from pydantic_settings import SettingsConfigDict

from service_oriented.application.config.base_config import BaseConfig
from service_oriented.deployment_environment import DeploymentEnvironment


TEST_DEPLOYMENT_ENVIRONMENT = DeploymentEnvironment(
    identifier="test",
    region="test",
    stage="test",
    vendor="test",
)


class ConfigWithoutEnvPrefix(BaseConfig):
    model_config = SettingsConfigDict(env_nested_delimiter="__")


class ConfigWithoutEnvNestedDelimiter(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="prefix_")


class ConfigWithAllTheThings(BaseConfig):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_prefix="test_",
    )


def test_env_nested_delimiter_is_required() -> None:
    with pytest.raises(RuntimeError) as exinfo:
        ConfigWithoutEnvNestedDelimiter(
            deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
        )
    assert RuntimeError == exinfo.type
    exception_message = str(exinfo.value)
    assert "env_nested_delimiter model config is required" == exception_message


def test_env_prefix_is_required() -> None:
    with pytest.raises(RuntimeError) as exinfo:
        ConfigWithoutEnvPrefix(deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT)
    assert RuntimeError == exinfo.type
    exception_message = str(exinfo.value)
    assert "env_prefix model config is required" == exception_message


def test_deployment_environment_is_accessible() -> None:
    config = ConfigWithAllTheThings(
        deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
    )
    deployment_environment = config.deployment_environment
    assert TEST_DEPLOYMENT_ENVIRONMENT == deployment_environment


def test_deployment_environment_is_required() -> None:
    with pytest.raises(ValidationError) as exinfo:
        ConfigWithAllTheThings()
    assert ValidationError == exinfo.type
    exception_message = str(exinfo.value)
    assert "1 validation error for ConfigWithAllTheThings" in exception_message
    assert "deployment_environment" in exception_message
    assert "Field required" in exception_message
