from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel

from wexample_helpers.const.types import FileStringOrPath
from wexample_helpers.helpers.file_helper import file_resolve_path

if TYPE_CHECKING:
    from wexample_filestate.file_state_manager import FileStateManager


class AbstractFileStateItem(BaseModel, ABC):
    state_manager: 'FileStateManager'
    path: FileStringOrPath
    _name: str

    def __init__(self, **data):
        path = file_resolve_path(data.get('path'))

        data['path'] = path
        _name = path.name

        super().__init__(**data)

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def get_item_title(self) -> str:
        pass

    def get_resolved(self):
        return self.path.resolve()

    @abstractmethod
    def is_file(self) -> bool:
        pass

    @abstractmethod
    def is_directory(self) -> bool:
        pass