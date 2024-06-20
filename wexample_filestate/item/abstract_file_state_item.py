from __future__ import annotations

from abc import ABC
from typing import Optional

from pydantic import BaseModel

from wexample_filestate.const.types import FileSystemStructurePermission
from wexample_helpers.const.types import FileStringOrPath
from wexample_helpers.helpers.file_helper import file_resolve_path


class AbstractFileStateItem(BaseModel, ABC):
    path: FileStringOrPath
    _name: str
    _mode: Optional[FileSystemStructurePermission] = None

    @property
    def name(self):
        return self._name

    @property
    def mode(self):
        return self._mode

    def __init__(self, **data):
        path = file_resolve_path(data.get('path'))

        data['path'] = path
        _name = path.name

        super().__init__(**data)

    def get_resolved(self):
        return self.path.resolve()
