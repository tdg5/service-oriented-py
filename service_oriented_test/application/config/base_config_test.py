import os
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest
from pydantic import ValidationError

from service_oriented.application.config.base_config import BaseConfig
from service_oriented.deployment_environment import DeploymentEnvironment


TEST_DEPLOYMENT_ENVIRONMENT = DeploymentEnvironment(
    identifier="test",
    region="test",
    stage="test",
    vendor="test",
)


class ConfigWithoutEnvNestedDelimiter(BaseConfig, env_prefix="prefix_"):
    pass


def test_env_nested_delimiter_is_required() -> None:
    with pytest.raises(RuntimeError) as exinfo:
        ConfigWithoutEnvNestedDelimiter(
            deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
        )
    assert RuntimeError == exinfo.type
    exception_message = str(exinfo.value)
    assert "env_nested_delimiter model config is required" == exception_message


class ConfigWithoutEnvPrefix(BaseConfig, env_nested_delimiter="__"):
    pass


def test_env_prefix_is_required() -> None:
    with pytest.raises(RuntimeError) as exinfo:
        ConfigWithoutEnvPrefix(deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT)
    assert RuntimeError == exinfo.type
    exception_message = str(exinfo.value)
    assert "env_prefix model config is required" == exception_message


class ConfigWithAllTheThings(
    BaseConfig,
    env_nested_delimiter="__",
    env_prefix="base_config_test_",
):
    pass


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


def test_yaml_config_path_is_accessible() -> None:
    yaml_config_path = "foo"
    config = ConfigWithAllTheThings(
        deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
        yaml_config_path=yaml_config_path,
    )
    assert yaml_config_path == config.yaml_config_path


def test_yaml_config_path_is_optional() -> None:
    config = ConfigWithAllTheThings(
        deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
    )
    assert config.yaml_config_path is None


class ConfigForTestingSourcePriorities(ConfigWithAllTheThings):
    layer_one: str
    layer_two: str
    layer_three: str
    layer_four: str
    layer_five: str


def test_setting_source_priorities() -> None:
    os.environ["BASE_CONFIG_TEST_LAYER_ONE"] = "env"
    os.environ["BASE_CONFIG_TEST_LAYER_TWO"] = "env"
    with TemporaryDirectory() as secrets_dir:
        for config_name in ["layer_one", "layer_two", "layer_three"]:
            with open(
                f"{secrets_dir}/base_config_test_{config_name}", "w+"
            ) as secret_file:
                secret_file.write("secret")
        with NamedTemporaryFile(mode="w+") as yaml_file:
            yaml_file.write(
                """
                layer_one: yaml
                layer_two: yaml
                layer_three: yaml
                layer_four: yaml
                """
            )
            yaml_file.flush()
            with NamedTemporaryFile(mode="w+") as dotenv_file:
                dotenv_file.write(
                    """
                    BASE_CONFIG_TEST_LAYER_ONE=dotenv
                    BASE_CONFIG_TEST_LAYER_TWO=dotenv
                    BASE_CONFIG_TEST_LAYER_THREE=dotenv
                    BASE_CONFIG_TEST_LAYER_FOUR=dotenv
                    BASE_CONFIG_TEST_LAYER_FIVE=dotenv
                    """
                )
                dotenv_file.flush()
                config = ConfigForTestingSourcePriorities(
                    _env_file=dotenv_file.name,
                    _secrets_dir=secrets_dir,
                    layer_one="init",
                    deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
                    yaml_config_path=yaml_file.name,
                )
                assert "init" == config.layer_one
                assert "env" == config.layer_two
                assert "secret" == config.layer_three
                assert "yaml" == config.layer_four
                assert "dotenv" == config.layer_five
