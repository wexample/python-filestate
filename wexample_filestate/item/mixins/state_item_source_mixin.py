from __future__ import annotations

from abc import abstractmethod

from wexample_filestate.item.abstract_file_state_item import AbstractFileStateItem


class StateItemSourceMixin:
    @abstractmethod
    def create_target(self) -> AbstractFileStateItem:
        pass
