from __future__ import annotations

import os
from typing import List
from wexample_filestate.item.abstract_file_state_item import AbstractFileStateItem
from wexample_filestate.item.file_state_item_file import FileStateItemFile


class FileStateItemDirectory(AbstractFileStateItem):
    _files: List[FileStateItemFile]
    _directories: List[FileStateItemDirectory]

    def get_resolved(self) -> str:
        return f'{super().get_resolved()}{os.sep}'
