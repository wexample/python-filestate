from __future__ import annotations

from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.helpers.state_item_helper import state_item_target_from_path
from wexample_filestate.item.file_state_item_directory import FileStateItemDirectory
from wexample_filestate.item.mixins.state_item_target_mixin import StateItemTargetMixin


class FileStateItemDirectoryTarget(FileStateItemDirectory, StateItemTargetMixin):
    config: StateItemConfig = None

    def configure(self, config: dict):
        base_path = self.get_resolved()

        if 'name' in config:
            _name = config['name']

        if 'children' in config:
            for item_config in config['children']:
                state_item_target_from_path(path=base_path, config=item_config)
