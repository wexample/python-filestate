from __future__ import annotations

from typing import Optional

from wexample_filestate.item.file_state_item_directory import FileStateItemDirectory
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
from wexample_filestate.item.mixins.state_item_target_mixin import StateItemTargetMixin


from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.helpers.state_item_helper import state_item_target_from_path

class FileStateItemDirectoryTarget(FileStateItemDirectory, StateItemTargetMixin):
    config: Optional[dict] = None

    def configure(self, config: dict):
        base_path = self.get_resolved()

        if 'name' in config:
            _name = config['name']

        if 'children' in config:
            for item_config in config['children']:
                print(item_config);
                state_item_target_from_path(path=base_path, config=item_config)
