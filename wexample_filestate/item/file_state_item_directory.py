from __future__ import annotations

import os
from typing import List
from wexample_filestate.item.abstract_file_state_item import AbstractFileStateItem
from wexample_filestate.item.file_state_item_file import FileStateItemFile


class FileStateItemDirectory(AbstractFileStateItem):
    _files: List[FileStateItemFile]
    _directories: List[FileStateItemDirectory]

    def configure(self, config: dict):
        base_path = self.get_resolved()

        if 'files' in config:
            for file in config['files']:
                FileStateItemFile(path=base_path + file['name'])

        if 'directories' in config:
            for directory in config['directories']:
                FileStateItemDirectory(path=base_path + directory['path'])

    def get_resolved(self) -> str:
        return f'{super()}{os.sep}'
