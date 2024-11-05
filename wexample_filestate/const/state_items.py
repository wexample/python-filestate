from typing import Union

from wexample_filestate.item.file_state_item_directory_source import (
    FileStateItemDirectorySource,
)
from wexample_filestate.item.file_state_item_directory_target import (
    FileStateItemDirectoryTarget,
)
from wexample_filestate.item.file_state_item_file_source import (
    FileStateItemFileSource,
)
from wexample_filestate.item.file_state_item_file_target import (
    FileStateItemFileTarget,
)

TargetFileOrDirectory = Union[FileStateItemDirectoryTarget, FileStateItemFileTarget]
SourceFileOrDirectory = Union[FileStateItemDirectorySource, FileStateItemFileSource]
