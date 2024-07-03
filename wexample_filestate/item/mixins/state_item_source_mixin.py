from __future__ import annotations

from wexample_filestate.item.abstract_file_state_item import AbstractStateItem
from wexample_helpers.helpers.file_helper import file_path_get_octal_mode
from wexample_helpers.const.types import FileStringOrPath


class StateItemSourceMixin:
    path: FileStringOrPath

    def get_octal_mode(self: AbstractStateItem) -> str:
        return file_path_get_octal_mode(self.path)
