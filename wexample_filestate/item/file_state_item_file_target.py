from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.item.abstract_file_state_item import AbstractFileStateItem


class FileStateItemFileTarget(AbstractFileStateItem):
    config: StateItemConfig = None
