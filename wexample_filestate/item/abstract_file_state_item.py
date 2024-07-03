from __future__ import annotations

from abc import abstractmethod
from pydantic import BaseModel
from wexample_helpers.const.types import FileStringOrPath


class AbstractStateItem(BaseModel):
    path: FileStringOrPath

    def get_resolved(self):
        return self.path.resolve()

    @abstractmethod
    def is_file(self) -> bool:
        pass

    @abstractmethod
    def is_directory(self) -> bool:
        pass
