from service_oriented.application.config import BaseConfig


class Config(
    BaseConfig,
    env_nested_delimiter="__",
    env_prefix="EXAMPLE_APPLICATION_",
):
    logging_config_yaml_path: str
