from __future__ import annotations

from wexample_filestate.item.abstract_file_state_item import AbstractFileStateItem
from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget


class FileStateItemDirectorySource(AbstractFileStateItem):
    def create_target(self) -> FileStateItemDirectoryTarget:
        return FileStateItemDirectoryTarget(path=self.path)