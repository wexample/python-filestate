from __future__ import annotations

from wexample_filestate.const.types_state_items import SourceFileOrDirectory, TargetFileOrDirectory
from wexample_filestate.options.abstract_option import AbstractOption
from wexample_filestate.options.class_option import ClassOption
from wexample_filestate.options.children_option import ChildrenOption
from wexample_filestate.options.git_option import GitOption
from wexample_filestate.options.mode_option import ModeOption
from wexample_filestate.options.mode_recursive_option import ModeRecursiveOption
from wexample_filestate.options.name_option import NameOption
from wexample_filestate.options.name_pattern_option import NamePatternOption
from wexample_filestate.options.remove_backup_max_file_size_option import RemoveBackupMaxFileSizeOption
from wexample_filestate.options.should_exist_option import ShouldExistOption
from wexample_filestate.options.type_option import TypeOption
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
ClassOption.model_rebuild()
ChildrenOption.model_rebuild()
GitOption.model_rebuild()
ModeOption.model_rebuild()
ModeRecursiveOption.model_rebuild()
NameOption.model_rebuild()
NamePatternOption.model_rebuild()
RemoveBackupMaxFileSizeOption.model_rebuild()
ShouldExistOption.model_rebuild()
TypeOption.model_rebuild()
FileStateItemFileTarget.model_rebuild()
FileStateItemDirectoryTarget.model_rebuild()
FileStateItemFileSource.model_rebuild()
FileStateItemDirectorySource.model_rebuild()
FileStateDryRunResult.model_rebuild()
FileStateResult.model_rebuild()
