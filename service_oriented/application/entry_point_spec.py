import sys
from typing import Protocol, Type, TypeVar


if sys.version_info >= (3, 10):  # pragma: no cover
    from typing import ParamSpec
else:  # pragma: no cover
    from typing_extensions import ParamSpec

from service_oriented.application.config import BaseConfig


P = ParamSpec("P")
C = TypeVar("C", bound=BaseConfig)


class _EntryPointClass(Protocol[P]):
    def __init__(self, config: C, *args: P.args, **kwargs: P.kwargs) -> None:
        pass  # pragma: no cover

    def run(self) -> None:
        pass  # pragma: no cover


class EntryPointSpec:
    def __init__(
        self,
        cls: Type[_EntryPointClass[P]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        self.args = args
        self.cls = cls
        self.kwargs = kwargs

    def build(self, config: C) -> _EntryPointClass:
        return self.cls(config, *self.args, **self.kwargs)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        args_strings = [f"{value!r}" for value in self.args]
        option_strings = [f"{key}={value!r}" for key, value in self.kwargs.items()]
        args_repr = ", ".join([self.cls.__name__] + args_strings + option_strings)
        return f"{class_name}({args_repr})"
