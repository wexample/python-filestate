from __future__ import annotations

from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.item.abstract_file_state_item import AbstractFileStateItem
from wexample_helpers.const.types import FileStringOrPath
from wexample_helpers.helpers.file_helper import file_resolve_path


def state_item_source_from_path(path: FileStringOrPath) -> AbstractFileStateItem:
    from wexample_filestate.item.file_state_item_directory_source import FileStateItemDirectorySource
    from wexample_filestate.item.file_state_item_file_source import FileStateItemFileSource
    resolved_path = file_resolve_path(path)
    if resolved_path.is_file():
        return FileStateItemFileSource(path=resolved_path)
    elif resolved_path.is_dir():
        return FileStateItemDirectorySource(path=resolved_path)
    else:
        raise ValueError('Root path should be a valid file or directory')


def state_item_target_from_path(path: FileStringOrPath, config: StateItemConfig) -> AbstractFileStateItem:
    from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
    from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
    resolved_path = file_resolve_path(path)

    if resolved_path.is_file() or ('type' in config and config['type'] == 'file'):
        return FileStateItemFileTarget(path=resolved_path, config=config)
    # Directories and undefined files.
    return FileStateItemDirectoryTarget(path=resolved_path, config=config)
