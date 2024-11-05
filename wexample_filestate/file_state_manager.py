from __future__ import annotations

from wexample_config.const.types import DictConfig
from wexample_filestate.item.item_target_directory import ItemTargetDirectory
from wexample_filestate.item.item_target_file import ItemTargetFile
from wexample_helpers.helpers.import_helper import import_dummy


class FileStateManager(ItemTargetDirectory):
    def __init__(self, config: DictConfig, **data):
        ItemTargetDirectory.__init__(self, value=None, **data)

        if config is not None:
            self.configure(config=config)

    def configure(self, config: DictConfig):
        super().configure(config=config)
        self.build_item_tree()


from wexample_filestate.result.abstract_result import AbstractResult
from wexample_filestate.const.state_items import TargetFileOrDirectory, SourceFileOrDirectory

import_dummy([AbstractResult, TargetFileOrDirectory, SourceFileOrDirectory])
ItemTargetFile.model_rebuild()
FileStateManager.model_rebuild()
