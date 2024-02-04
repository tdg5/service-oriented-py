import os
from typing import Any, Dict, List, Optional, Tuple, Type

import yaml
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource


class YamlConfigSettingsSource(PydanticBaseSettingsSource):
    @classmethod
    def get_yaml_config_path_from_sources(
        cls,
        sources: List[PydanticBaseSettingsSource],
    ) -> Optional[str]:
        for source in sources:
            config_from_source = source()
            yaml_config_path = config_from_source.get("yaml_config_path")
            if yaml_config_path:
                return str(yaml_config_path)
        return None

    @classmethod
    def from_sources(
        cls,
        settings_cls: Type[BaseSettings],
        sources: List[PydanticBaseSettingsSource],
    ) -> "YamlConfigSettingsSource":
        yaml_config_path = YamlConfigSettingsSource.get_yaml_config_path_from_sources(
            sources=sources,
        )

        return YamlConfigSettingsSource(
            settings_cls=settings_cls,
            yaml_config_path=yaml_config_path,
        )

    def __init__(
        self,
        settings_cls: Type[BaseSettings],
        yaml_config_path: Optional[str] = None,
    ) -> None:
        super().__init__(settings_cls)

        self._yaml_config: Dict[str, Any] = self._load_yaml_config(yaml_config_path)

    def _load_yaml_config(self, yaml_config_path: Optional[str]) -> Dict[str, Any]:
        if not yaml_config_path or not os.path.exists(yaml_config_path):
            return {}

        with open(yaml_config_path, mode="r", encoding="utf-8") as stream:
            yaml_config = yaml.safe_load(stream)

        return yaml_config if isinstance(yaml_config, dict) else {}

    def get_field_value(
        self,
        field: FieldInfo,
        field_name: str,
    ) -> Tuple[Any, str, bool]:
        # We're not required to do anything here. Implement return to make mypy happy.
        return None, "", False

    def __call__(self) -> Dict[str, Any]:
        return self._yaml_config
