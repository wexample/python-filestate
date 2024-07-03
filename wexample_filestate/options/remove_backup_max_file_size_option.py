from typing import Type
from types import UnionType

from wexample_filestate.options.abstract_option import AbstractOption

REMOVE_BACKUP_MAX_FILE_SIZE_DEFAULT: int = 1000


class RemoveBackupMaxFileSizeOption(AbstractOption):
    value: int = REMOVE_BACKUP_MAX_FILE_SIZE_DEFAULT

    @staticmethod
    def get_name() -> str:
        return "remove_backup_max_file_size"

    @staticmethod
    def get_value_type() -> Type | UnionType:
        return int
