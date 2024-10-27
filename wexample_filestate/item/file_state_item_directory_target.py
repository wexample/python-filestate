from __future__ import annotations


import os
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
        from wexample_helpers.helpers.directory_helper import directory_get_base_name

        config = config or {}

        # If path is a file, ignore file name a keep parent directory.
        if os.path.isfile(path):
            path = os.path.dirname(path)

        config["name"] = directory_get_base_name(path)

        return cls(
            config=config,
        )
