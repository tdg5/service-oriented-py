from typing import Generic, Optional, Type, TypeVar, get_args

from typing_extensions import get_original_bases

from service_oriented.application.base_application import BaseApplication
from service_oriented.application.config import BaseConfig


C = TypeVar("C", bound=BaseConfig)
A = TypeVar("A", bound=BaseApplication)


# TODO: The type annotation isn't quite right here because there's no
# requirement that A is A[C].
class GenericMain(Generic[C, A]):
    def __init__(self, config: Optional[C] = None) -> None:
        self.config = config or self._build_config()
        self.application = self._build_application(self.config)

    @classmethod
    def application_class(cls) -> Type[A]:
        for base in get_original_bases(cls):
            base_args = get_args(base)
            if base_args and issubclass(base_args[1], BaseApplication):
                application_class: Type[A] = base_args[1]
                return application_class
        raise RuntimeError(f"Unable to determine application class for {cls}")

    @classmethod
    def config_class(cls) -> Type[C]:
        for base in get_original_bases(cls):
            base_args = get_args(base)
            if base_args and issubclass(base_args[0], BaseConfig):
                config_class: Type[C] = base_args[0]
                return config_class
        raise RuntimeError(f"Unable to determine config class for {cls}")

    def _build_application(self, config: C) -> A:
        return self.application_class()(config=config)

    def _build_config(self) -> C:
        return self.config_class()()

    def run(self) -> None:
        self.application.run()
