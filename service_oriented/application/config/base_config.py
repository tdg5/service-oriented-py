from typing import Any, Optional, Tuple, Type

from pydantic import BeforeValidator, ValidationInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource
from typing_extensions import Annotated

from service_oriented.application.config.yaml_config_settings_source import (
    YamlConfigSettingsSource,
)
from service_oriented.deployment_environment import DeploymentEnvironment


def handle_alternative_deployment_environment_formats(
    value: Any,
    info: ValidationInfo,
) -> Any:
    if isinstance(value, str):
        return DeploymentEnvironment.from_stub(value)
    elif isinstance(value, dict):
        if (
            isinstance(identifier := value.get("identifier"), str)
            and isinstance(region := value.get("region"), str)
            and isinstance(stage := value.get("stage"), str)
            and isinstance(vendor := value.get("vendor"), str)
        ):
            return DeploymentEnvironment(
                identifier=identifier,
                region=region,
                stage=stage,
                vendor=vendor,
            )

    return value


class BaseConfig(BaseSettings):
    deployment_environment: Annotated[
        DeploymentEnvironment,
        BeforeValidator(handle_alternative_deployment_environment_formats),
    ]
    entry_point: str
    yaml_config_path: Optional[str] = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not self.model_config.get("env_nested_delimiter"):
            raise RuntimeError("env_nested_delimiter model config is required")

        if not self.model_config.get("env_prefix"):
            raise RuntimeError("env_prefix model config is required")

        super().__init__(*args, **kwargs)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        yaml_config_settings = YamlConfigSettingsSource.from_sources(
            settings_cls=settings_cls,
            sources=[
                init_settings,
                env_settings,
                file_secret_settings,
                dotenv_settings,
            ],
        )

        return (
            init_settings,
            env_settings,
            file_secret_settings,
            yaml_config_settings,
            dotenv_settings,
        )
