from abc import ABC, abstractmethod
from types import UnionType
from typing import Any, Type, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from wexample_filestate.const.types import StateItemConfig
    from wexample_filestate.const.types_state_items import TargetFileOrDirectory


class AbstractOption(BaseModel, ABC):
    value: Any
    target: "TargetFileOrDirectory"

    def __init__(self, value: Any, target: "TargetFileOrDirectory") -> None:
        value_type = self.get_value_type()
        if not isinstance(value, value_type):
            from wexample_filestate.const.exceptions import InvalidOptionTypeException
            raise InvalidOptionTypeException(
                f'Invalid type for option "{self.get_name()}": '
                f'{value_type(value)}, '
                f'expected {value_type}')

        super().__init__(
            value=value,
            target=target
        )

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_value_type() -> Type | UnionType:
        pass

    @staticmethod
    def resolve_config(config: "StateItemConfig") -> "StateItemConfig":
        return config
