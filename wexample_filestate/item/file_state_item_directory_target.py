from __future__ import annotations

from typing import Optional

from wexample_config.const.types import StateItemConfig
from wexample_filestate.item.file_state_item_directory import FileStateItemDirectory
from wexample_filestate.item.mixins.state_item_target_mixin import StateItemTargetMixin


class FileStateItemDirectoryTarget(FileStateItemDirectory, StateItemTargetMixin):
    @classmethod
    def create_from_path(
        cls,
        path: str,
        config: Optional[StateItemConfig] = None,
    ) -> FileStateItemDirectoryTarget:
        config = config or {}

        return cls(
        )
