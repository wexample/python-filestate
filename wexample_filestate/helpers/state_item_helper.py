from wexample_filestate.item.abstract_file_state_item import AbstractFileStateItem
from wexample_filestate.item.file_state_item_directory_source import FileStateItemDirectorySource
from wexample_filestate.item.file_state_item_file_source import FileStateItemFileSource
from wexample_helpers.helpers.file_helper import file_resolve_path


def state_item_from_path(path) -> AbstractFileStateItem:
    resolved_path = file_resolve_path(path)
    if resolved_path.is_file():
        return FileStateItemFileSource(path=resolved_path)
    elif resolved_path.is_dir():
        return FileStateItemDirectorySource(path=resolved_path)
    else:
        raise ValueError('Root path should be a valid file or directory')
