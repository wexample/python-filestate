from __future__ import annotations

from wexample_filestate.item.abstract_file_state_item import AbstractFileStateItem
from wexample_helpers.helpers.file_helper import file_path_get_octal_mode


class StateItemSourceMixin:
    def get_octal_mode(self: AbstractFileStateItem) -> str:
        return file_path_get_octal_mode(self.path)
