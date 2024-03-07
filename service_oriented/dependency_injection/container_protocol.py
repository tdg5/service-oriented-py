from typing import Any, Protocol, Type, TypeVar, Union

from rodi import Container
from typing_extensions import Self


T = TypeVar("T")


# This comes from rodi, but is replicated here to better encapsulate use of rodi
# https://github.com/Neoteroi/rodi/blob/3e358241ccdb0910a32ff519ae1708f84845e06c/rodi/__init__.py#L38
class ContainerProtocol(Protocol):
    """
    Generic interface of DI Container that can register and resolve services,
    and tell if a type is configured.
    """

    def register(self, obj_type: Union[Type, str], *args: Any, **kwargs: Any) -> Self:
        """Registers a type in the container, with optional arguments."""

    def resolve(self, obj_type: Union[Type[T], str], *args: Any, **kwargs: Any) -> T:
        """Activates an instance of the given type, with optional arguments."""

    def __contains__(self, item: Any) -> bool:
        """
        Returns a value indicating whether a given type is configured in this container.
        """


container: ContainerProtocol = Container()
