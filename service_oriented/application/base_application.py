from typing import Any, Dict, Generic, Optional, TypeVar

from service_oriented.application.config import BaseConfig
from service_oriented.application.entry_point_spec import EntryPointSpec


C = TypeVar("C", bound=BaseConfig)


class BaseApplication(Generic[C]):
    default_entry_points: Dict[str, EntryPointSpec] = {}

    @classmethod
    def __init_subclass__(
        cls,
        entry_points: Optional[Dict[str, EntryPointSpec]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init_subclass__(**kwargs)
        _entry_points = entry_points or {}
        cls.default_entry_points = _entry_points

    def __init__(
        self,
        config: C,
        entry_points: Optional[Dict[str, EntryPointSpec]] = None,
    ) -> None:
        self.config: C = config
        _entry_points = entry_points or {}
        self.entry_points = {**self.default_entry_points, **_entry_points}

    def run(self) -> None:
        entry_point_name = self.config.entry_point
        entry_point_spec = self.entry_points.get(entry_point_name)
        if entry_point_spec is None:
            raise RuntimeError(
                f"No mapping found for entry point named '{entry_point_name}'"
            )
        entry_point = entry_point_spec.build(config=self.config)
        entry_point.run()
