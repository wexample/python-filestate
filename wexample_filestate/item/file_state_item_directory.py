from __future__ import annotations

import os
from wexample_filestate.item.abstract_file_state_item import AbstractStateItem


class FileStateItemDirectory(AbstractStateItem):
    def get_item_title(self) -> str:
        return 'Directory'

    def get_resolved(self) -> str:
        return f'{super().get_resolved()}{os.sep}'

    def is_file(self) -> bool:
        return False

    def is_directory(self) -> bool:
        return True
