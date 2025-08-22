from __future__ import annotations

from wexample_config.const.types import DictConfig
from wexample_filestate.item.item_target_directory import ItemTargetDirectory
from wexample_filestate.item.item_target_file import ItemTargetFile
from wexample_helpers.helpers.polyfill import polyfill_import, polyfill_register_global


class FileStateManager(ItemTargetDirectory):
    def __init__(self, **data) -> None:
        super().__init__(value=None, **data)

    def configure(self, config: DictConfig) -> None:
        super().configure(config=config)

        # As root
        self.build_item_tree()


from wexample_filestate.const.state_items import (
    SourceFileOrDirectory,
    TargetFileOrDirectory,
)
from wexample_filestate.result.abstract_result import AbstractResult

polyfill_import([TargetFileOrDirectory, SourceFileOrDirectory])
polyfill_register_global([AbstractResult])
ItemTargetFile.model_rebuild()
FileStateManager.model_rebuild()
