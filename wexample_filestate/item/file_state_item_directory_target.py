from __future__ import annotations

from typing import Optional

from wexample_config.const.types import DictConfig
from wexample_filestate.item.file_state_item_directory import FileStateItemDirectory
from wexample_filestate.item.mixins.state_item_target_mixin import StateItemTargetMixin
from wexample_helpers.const.types import FileStringOrPath
from wexample_helpers.helpers.directory_helper import (
    directory_get_base_name,
    directory_get_parent_path,
)


class FileStateItemDirectoryTarget(StateItemTargetMixin, FileStateItemDirectory):
    def __init__(self, config: DictConfig, **data):
        StateItemTargetMixin.__init__(self, config=config, **data)

    def configure_from_file(self, path: FileStringOrPath):
        from wexample_helpers_yaml.helpers.yaml_helpers import yaml_read

        if yaml_read is not None:
            self.set_value(raw_value=yaml_read(str(path)))

    @classmethod
    def create_from_path(
        cls,
        path: str,
        config: Optional[DictConfig] = None,
    ) -> FileStateItemDirectoryTarget:
        config = config or {}

        config["name"] = directory_get_base_name(path)
        return cls(
            config=config,
            base_path=directory_get_parent_path(path),
        )
