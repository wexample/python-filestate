from __future__ import annotations

from wexample_filestate.item.file_state_item_directory import FileStateItemDirectory
from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
from wexample_filestate.item.mixins.state_item_source_mixin import StateItemSourceMixin


class FileStateItemDirectorySource(FileStateItemDirectory, StateItemSourceMixin):
    def create_target(self) -> FileStateItemDirectoryTarget:
        return FileStateItemDirectoryTarget(
            state_manager=self.state_manager,
            path=self.path
        )
