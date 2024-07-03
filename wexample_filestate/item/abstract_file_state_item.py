from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING
from pydantic import BaseModel


if TYPE_CHECKING:
    from wexample_helpers.const.types import FileStringOrPath


class AbstractStateItem(BaseModel):
    path: "FileStringOrPath"

    def get_resolved(self):
        return self.path.resolve()

    @abstractmethod
    def is_file(self) -> bool:
        pass

    @abstractmethod
    def is_directory(self) -> bool:
        pass
