from __future__ import annotations

from wexample_filestate.item.file_state_item_file import FileStateItemFile
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
from wexample_filestate.item.mixins.state_item_source_mixin import StateItemSourceMixin


class FileStateItemFileSource(FileStateItemFile, StateItemSourceMixin):
    def create_target(self) -> FileStateItemFileTarget:
        return FileStateItemFileTarget(path=self.path)
