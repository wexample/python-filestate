from __future__ import annotations

from wexample_filestate.item.file_state_item_directory import FileStateItemDirectory
from wexample_filestate.item.mixins.state_item_target_mixin import StateItemTargetMixin


class FileStateItemDirectoryTarget(FileStateItemDirectory, StateItemTargetMixin):
    @classmethod
    def create_from_path(
        cls,
        path: str,
    ) -> FileStateItemDirectoryTarget:
        return cls(
        )
