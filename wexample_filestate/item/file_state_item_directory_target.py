from __future__ import annotations

from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.item.abstract_file_state_item import AbstractFileStateItem


class FileStateItemDirectoryTarget(AbstractFileStateItem):
    config: StateItemConfig = None
