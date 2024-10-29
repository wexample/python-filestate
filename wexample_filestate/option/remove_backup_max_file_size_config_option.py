from typing import Type
from types import UnionType

from wexample_filestate.option.abstract_item_config_option import AbstractItemConfigOption

REMOVE_BACKUP_MAX_FILE_SIZE_DEFAULT: int = 1000


class RemoveBackupMaxFileSizeConfigOption(AbstractItemConfigOption):
    value: int = REMOVE_BACKUP_MAX_FILE_SIZE_DEFAULT

    @staticmethod
    def get_value_allowed_type() -> Type | UnionType:
        return int
