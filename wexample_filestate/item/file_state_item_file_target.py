from typing import Optional

from wexample_filestate.item.file_state_item_file import FileStateItemFile
from wexample_filestate.item.mixins.state_item_target_mixin import StateItemTargetMixin


class FileStateItemFileTarget(FileStateItemFile, StateItemTargetMixin):
    config: Optional[dict] = None

    def __init__(self, **data):
        super().__init__(**data)
        StateItemTargetMixin.__init__(self, **data)
