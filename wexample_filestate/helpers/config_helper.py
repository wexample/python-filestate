from wexample_filestate.const.enums import DiskItemType
from wexample_filestate.const.types import StateItemConfig
from wexample_helpers.const.types import FileStringOrPath
from wexample_helpers.helpers.file_helper import file_resolve_path


def config_has_item_type(config: StateItemConfig, path: FileStringOrPath) -> bool:
    resolved_path = file_resolve_path(path)

    if resolved_path.is_file() and config["type"] == DiskItemType.FILE:
        return True

    if resolved_path.is_dir() and config["type"] == DiskItemType.DIRECTORY:
        return True

    return False
