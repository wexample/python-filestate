from __future__ import annotations

from typing import Optional

from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.const.types_state_items import SourceFileOrDirectory, TargetFileOrDirectory
from wexample_filestate.options.abstract_option import AbstractOption
from wexample_filestate.result.file_state_dry_run_result import FileStateDryRunResult
from wexample_filestate.result.file_state_result import FileStateResult
from wexample_helpers.const.types import FileStringOrPath
from wexample_helpers.helpers.directory_helper import directory_get_base_name, directory_get_parent_path
from wexample_prompt.io_manager import IOManager
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
from wexample_filestate.item.file_state_item_file_source import FileStateItemFileSource
from wexample_filestate.item.file_state_item_directory_source import FileStateItemDirectorySource

class FileStateManager(FileStateItemDirectoryTarget):
    def __init__(self, root: FileStringOrPath, config: Optional[StateItemConfig] = None,
                 io: Optional[IOManager] = None):
        config["name"] = directory_get_base_name(root)

        super().__init__(
            config=config,
            base_path=directory_get_parent_path(root),
            io=io or IOManager()
        )

        if config:
            self.configure(config)


# Rebuild classes that point back to manager.
AbstractOption.model_rebuild()
FileStateItemFileTarget.model_rebuild()
FileStateItemDirectoryTarget.model_rebuild()
FileStateItemFileSource.model_rebuild()
FileStateItemDirectorySource.model_rebuild()
FileStateDryRunResult.model_rebuild()
FileStateResult.model_rebuild()
