from __future__ import annotations

from wexample_filestate.item.abstract_state_item import AbstractStateItem


class FileStateItemFile(AbstractStateItem):
    def get_item_title(self) -> str:
        return "File"

    def is_file(self) -> bool:
        return True

    def is_directory(self) -> bool:
        return False
