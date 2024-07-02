from abc import ABC, abstractmethod
from types import UnionType
from typing import Any, Type

from pydantic import BaseModel

from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.const.types_state_items import TargetFileOrDirectory


class AbstractOption(BaseModel, ABC):
    value: Any
    target: "TargetFileOrDirectory"

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_value_type() -> Type | UnionType:
        pass

    @staticmethod
    def resolve_config(config: StateItemConfig) -> StateItemConfig:
        return config
