import os
from typing import List, Optional
from pydantic import BaseModel
from wexample_filestate.const.disk import DiskItemType
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget


class ChildConfig(BaseModel):
    config: Optional[dict] = None

    def parse_config(self, target) -> List:
        base_path = target.get_resolved()
        item_name = self.config.get("name")
        is_file_type = self.config.get("type") == DiskItemType.FILE
        is_actual_file = isinstance(item_name, str) and os.path.isfile(os.path.join(base_path, item_name))

        if is_file_type or is_actual_file:
            state_item = FileStateItemFileTarget(base_path=base_path, config=self.config, parent=self)
        else:
            state_item = FileStateItemDirectoryTarget(base_path=base_path, config=self.config, parent=self)

        return [state_item]

