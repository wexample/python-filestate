from __future__ import annotations

from typing import Any, Optional

from wexample_config.const.types import DictConfig
from wexample_filestate.item.file_state_item_file import FileStateItemFile
from wexample_filestate.item.mixins.state_item_target_mixin import \
    StateItemTargetMixin


class FileStateItemFileTarget(StateItemTargetMixin, FileStateItemFile):
    config: Optional[DictConfig] = None

    def __init__(self, **data):
        FileStateItemFile.__init__(self, **data)
        StateItemTargetMixin.__init__(self, **data)
