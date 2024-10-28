from typing import Type
from types import UnionType

from wexample_filestate.option.abstract_item_option import AbstractItemOption

REMOVE_BACKUP_MAX_FILE_SIZE_DEFAULT: int = 1000


class RemoveBackupMaxFileSizeOption(AbstractItemOption):
    value: int = REMOVE_BACKUP_MAX_FILE_SIZE_DEFAULT

    @staticmethod
    def get_value_type() -> Type | UnionType:
        return int
