import os
from logging import config as logging_config
from typing import Dict

import yaml
from dependency_injector.resources import Resource


class LoggingConfigResource(Resource):
    def init(self, yaml_path: str) -> None:
        config = self._load_yaml_config(yaml_path=yaml_path)
        if config:
            logging_config.dictConfig(config)

    def shutdown(self, none: None) -> None:
        pass

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
