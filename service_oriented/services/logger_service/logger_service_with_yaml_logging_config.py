import logging
import os
from logging import Logger
from logging import config as logging_config
from typing import Dict

import yaml

from service_oriented.services.logger_service.logger_service import LoggerService


class LoggerServiceWithYamlLoggingConfig(LoggerService):
    def __init__(self, yaml_path: str) -> None:
        config = self._load_yaml_config(yaml_path=yaml_path)
        if config:
            logging_config.dictConfig(config)

    def _load_yaml_config(self, yaml_path: str) -> Dict:
        if not os.path.exists(yaml_path):
            return {}

        with open(yaml_path, encoding="utf-8", mode="r") as stream:
            config = yaml.safe_load(stream)

        if not isinstance(config, Dict):
            raise ValueError(
                f"Expected logging config dict, received {config.__class__}: {config}"
            )

        return config

    def get_logger(self, name: str) -> Logger:
        return logging.getLogger(name)
