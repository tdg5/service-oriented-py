"""
Tests for YamlConfigSettingsSource integration with pydantic.
"""

import os
import textwrap
from tempfile import NamedTemporaryFile
from typing import Any, Dict, Optional, Tuple, Type

from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

from service_oriented.application.config.yaml_config_settings_source import (
    YamlConfigSettingsSource,
)


YAML_TEMPLATE = """
a_str: '{a_str}'
an_int: {an_int}
a_dict:
    a_str: '{a_str}'
    an_int: {an_int}
"""


class YamlConfigTestConfig(BaseSettings):
    """
    Test configuration class that is configured to load config from yaml.
    """

    a_str: str
    an_int: int
    a_dict: Dict[str, Any]
    yaml_config_path: Optional[str] = None

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
            ],
        )
        return (
            # Include a built-in settings source for extra validation
            init_settings,
            yaml_config_settings,
        )


def test_yaml_config_settings_source_loads_init_yaml_config_as_expected() -> None:
    """
    Test the the yaml config path can be taken from the init settings and that
    the config is loaded from yaml as expected.
    """
    a_str: str = "A man a plan, a canal, panama"
    an_int: int = 5
    yaml = YAML_TEMPLATE.format(a_str=a_str, an_int=an_int)
    with NamedTemporaryFile(mode="w+") as temp_file:
        temp_file.write(textwrap.dedent(yaml))
        temp_file.flush()
        config = YamlConfigTestConfig(yaml_config_path=temp_file.name)
        assert a_str == config.a_str
        assert an_int == config.an_int
        assert a_str == config.a_dict["a_str"]
        assert an_int == config.a_dict["an_int"]


def test_yaml_config_settings_source_loads_config_yaml_config_as_expected() -> None:
    """
    Test that the yaml config path can come from other settings sources if no
    yaml config path is given as an argument to init and the config is loaded
    as expected.
    """
    a_str: str = "taco cat"
    an_int: int = 42
    yaml = YAML_TEMPLATE.format(a_str=a_str, an_int=an_int)
    with NamedTemporaryFile(mode="w+") as temp_file:
        temp_file.write(textwrap.dedent(yaml))
        temp_file.flush()
        os.environ["YAML_CONFIG_PATH"] = temp_file.name
        config = YamlConfigTestConfig()
        assert a_str == config.a_str
        assert an_int == config.an_int
        assert a_str == config.a_dict["a_str"]
        assert an_int == config.a_dict["an_int"]
