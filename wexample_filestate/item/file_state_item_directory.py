from __future__ import annotations

from wexample_filestate.item.abstract_state_item import AbstractStateItem


class FileStateItemDirectory(AbstractStateItem):
    def get_item_title(self) -> str:
        return "Directory"
