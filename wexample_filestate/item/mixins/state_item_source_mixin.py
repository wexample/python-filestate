from __future__ import annotations

from abc import abstractmethod

from wexample_filestate.item.abstract_file_state_item import AbstractFileStateItem
from wexample_helpers.helpers.file_helper import file_mode_num_to_octal


class StateItemSourceMixin:
    @abstractmethod
    def create_target(self) -> AbstractFileStateItem:
        pass

    def get_octal_mode(self: AbstractFileStateItem) -> str:
        return file_mode_num_to_octal(self.path.stat().st_mode)
