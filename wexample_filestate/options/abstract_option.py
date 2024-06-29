from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from wexample_filestate.const.types_state_items import TargetFileOrDirectory


class AbstractOption(BaseModel, ABC):
    value: Any
    target: "TargetFileOrDirectory"

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        pass
