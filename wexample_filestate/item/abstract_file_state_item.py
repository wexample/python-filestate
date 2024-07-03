from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from wexample_filestate.file_state_manager_child import AbstractFileStateManagerChild

if TYPE_CHECKING:
    from wexample_helpers.const.types import FileStringOrPath


class AbstractStateItem(AbstractFileStateManagerChild):
    path: "FileStringOrPath"

    def get_resolved(self):
        return self.path.resolve()

    @abstractmethod
    def is_file(self) -> bool:
        pass

    @abstractmethod
    def is_directory(self) -> bool:
        pass
