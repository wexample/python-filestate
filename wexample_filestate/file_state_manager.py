from __future__ import annotations

from wexample_filestate.const.types_state_items import SourceFileOrDirectory, TargetFileOrDirectory
from wexample_filestate.options.abstract_option import AbstractOption
from wexample_filestate.result.file_state_dry_run_result import FileStateDryRunResult
from wexample_filestate.result.file_state_result import FileStateResult
from wexample_helpers.const.types import FileStringOrPath
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
from wexample_filestate.item.file_state_item_file_source import FileStateItemFileSource
from wexample_filestate.item.file_state_item_directory_source import FileStateItemDirectorySource


class FileStateManager(FileStateItemDirectoryTarget):
    """
    This is not more than an alias and an entrypoint for main modules loads.
    """
    pass


# Rebuild classes that point back to manager.
AbstractOption.model_rebuild()
FileStateItemFileTarget.model_rebuild()
FileStateItemDirectoryTarget.model_rebuild()
FileStateItemFileSource.model_rebuild()
FileStateItemDirectorySource.model_rebuild()
FileStateDryRunResult.model_rebuild()
FileStateResult.model_rebuild()
