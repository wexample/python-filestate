from __future__ import annotations

from wexample_filestate.item.file_state_item_directory_target import \
    FileStateItemDirectoryTarget
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
from wexample_helpers.helpers.import_helper import import_dummy


class FileStateManager(FileStateItemDirectoryTarget):
    """
    This is not more than an alias and an entrypoint for main modules loads.
    """

    pass


from wexample_filestate.result.abstract_result import AbstractResult
import_dummy(AbstractResult)
FileStateItemFileTarget.model_rebuild()
