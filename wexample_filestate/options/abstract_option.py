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

        if hasattr(value_type, '__args__'):
            expected_types = value_type.__args__
        else:
            expected_types = (value_type,)

        valid = False
        for expected_type in expected_types:
            if isinstance(expected_type, type):
                if isinstance(value, expected_type) or (isinstance(value, type) and issubclass(value, expected_type)):
                    valid = True
                    break
            else:
                if isinstance(value, expected_type):
                    valid = True
                    break

        if not valid:
            from wexample_filestate.const.exceptions import InvalidOptionTypeException
            raise InvalidOptionTypeException(
                f'Invalid type for option "{self.get_name()}": '
                f'{type(value)}, '
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
