from __future__ import annotations

from typing import Optional

from wexample_filestate.item.file_state_item_directory import FileStateItemDirectory
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
from wexample_filestate.item.mixins.state_item_target_mixin import StateItemTargetMixin


class FileStateItemDirectoryTarget(FileStateItemDirectory, StateItemTargetMixin):
    config: Optional[dict] = None

    def configure(self, config: dict):
        base_path = self.get_resolved()

        if 'name' in config:
            _name = config['name']

        if 'files' in config:
            for item_config in config['files']:
                FileStateItemFileTarget(path=base_path + item_config['name'], config=item_config)

        if 'directories' in config:
            for item_config in config['directories']:
                FileStateItemDirectoryTarget(path=base_path + item_config['path'], config=item_config)
