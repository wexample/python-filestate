from __future__ import annotations

from typing import Optional

from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_helpers.helpers.import_helper import import_dummy


class FileStateManager(FileStateItemDirectoryTarget):
    """
    This is not more than an alias and an entrypoint for main modules loads.
    """
    pass

import_dummy([Optional, AbstractOperation])
FileStateManager.model_rebuild()
