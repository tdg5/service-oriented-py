from typing import Any, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

from service_oriented.deployment_environment import DeploymentEnvironment


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict()

    deployment_environment: DeploymentEnvironment

    def __init__(self, *args: Any, **kwargs: Any):
        if not self.model_config.get("env_nested_delimiter"):
            raise RuntimeError("env_nested_delimiter model config is required")

        if not self.model_config.get("env_prefix"):
            raise RuntimeError("env_prefix model config is required")

        super().__init__(*args, **kwargs)
