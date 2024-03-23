import os
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest
from pydantic import ValidationError

from service_oriented_test.example_application.app.config import Config
from service_oriented_test.test_helpers import TEST_DEPLOYMENT_ENVIRONMENT


def test_deployment_environment_is_accessible() -> None:
    config = Config(
        deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
        entry_point="test",
        logging_config_yaml_path="logging_config.yaml",
    )
    deployment_environment = config.deployment_environment
    assert TEST_DEPLOYMENT_ENVIRONMENT == deployment_environment


def test_deployment_environment_is_required() -> None:
    with pytest.raises(ValidationError) as exinfo:
        Config(
            entry_point="test",
            logging_config_yaml_path="logging_config.yaml",
        )
    assert ValidationError == exinfo.type
    exception_message = str(exinfo.value)
    assert "1 validation error for Config" in exception_message
    assert "deployment_environment" in exception_message
    assert "Field required" in exception_message


def test_logging_config_yaml_path_is_accessible() -> None:
    logging_config_yaml_path = "logging_config.yaml"
    config = Config(
        deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
        entry_point="test",
        logging_config_yaml_path=logging_config_yaml_path,
    )
    assert logging_config_yaml_path == config.logging_config_yaml_path


def test_logging_config_yaml_path_is_required() -> None:
    with pytest.raises(ValidationError) as exinfo:
        Config(
            deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
            entry_point="test",
        )
    assert ValidationError == exinfo.type
    exception_message = str(exinfo.value)
    assert "1 validation error for Config" in exception_message
    assert "logging_config_yaml_path" in exception_message
    assert "Field required" in exception_message


def test_yaml_config_path_is_accessible() -> None:
    yaml_config_path = "foo"
    config = Config(
        deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
        entry_point="test",
        logging_config_yaml_path="logging_config.yaml",
        yaml_config_path=yaml_config_path,
    )
    assert yaml_config_path == config.yaml_config_path


def test_yaml_config_path_is_optional() -> None:
    config = Config(
        deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
        entry_point="test",
        logging_config_yaml_path="logging_config.yaml",
    )
    assert config.yaml_config_path is None


class ConfigForTestingSourcePriorities(Config):
    layer_one: str
    layer_two: str
    layer_three: str
    layer_four: str
    layer_five: str


def test_setting_source_priorities() -> None:
    os.environ["EXAMPLE_APPLICATION_LAYER_ONE"] = "env"
    os.environ["EXAMPLE_APPLICATION_LAYER_TWO"] = "env"
    with TemporaryDirectory() as secrets_dir:
        for config_name in ["layer_one", "layer_two", "layer_three"]:
            with open(
                f"{secrets_dir}/example_application_{config_name}", "w+"
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
                    EXAMPLE_APPLICATION_LAYER_ONE=dotenv
                    EXAMPLE_APPLICATION_LAYER_TWO=dotenv
                    EXAMPLE_APPLICATION_LAYER_THREE=dotenv
                    EXAMPLE_APPLICATION_LAYER_FOUR=dotenv
                    EXAMPLE_APPLICATION_LAYER_FIVE=dotenv
                    """
                )
                dotenv_file.flush()
                config = ConfigForTestingSourcePriorities(
                    _env_file=dotenv_file.name,
                    _secrets_dir=secrets_dir,
                    entry_point="test",
                    layer_one="init",
                    deployment_environment=TEST_DEPLOYMENT_ENVIRONMENT,
                    logging_config_yaml_path="logging_config.yaml",
                    yaml_config_path=yaml_file.name,
                )
                assert "init" == config.layer_one
                assert "env" == config.layer_two
                assert "secret" == config.layer_three
                assert "yaml" == config.layer_four
                assert "dotenv" == config.layer_five
