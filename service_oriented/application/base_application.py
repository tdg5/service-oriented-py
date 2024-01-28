from typing import Dict, Generic, TypeVar

from service_oriented.application.config import BaseConfig
from service_oriented.application.entry_point_spec import EntryPointSpec


C = TypeVar("C", bound=BaseConfig)
E = TypeVar("E", bound=EntryPointSpec)


class BaseApplication(Generic[C]):
    def __init__(
        self,
        config: C,
        entry_points: Dict[str, E],
    ):
        self.config: C = config
        self.entry_points: Dict[str, E] = entry_points

    def run(self) -> None:
        entry_point_name = self.config.entry_point
        entry_point_spec = self.entry_points.get(entry_point_name)
        if entry_point_spec is None:
            raise RuntimeError(
                f"No mapping found for entry point named '{entry_point_name}'"
            )
        entry_point = entry_point_spec.build(config=self.config)
        entry_point.run()
