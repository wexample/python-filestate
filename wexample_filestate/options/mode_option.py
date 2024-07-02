from typing import Type, Union
from types import UnionType
from wexample_filestate.const.types import FileSystemPermission
from wexample_filestate.options.abstract_option import AbstractOption
from wexample_helpers.helpers.file_helper import file_mode_octal_to_num


class ModeOption(AbstractOption):
    value: FileSystemPermission

    @staticmethod
    def get_name() -> str:
        return "mode"

    @staticmethod
    def get_value_type() -> Type | UnionType:
        return Union[str, int]

    def get_octal(self) -> str:
        if isinstance(self.value, str):
            return self.value
        elif isinstance(self.value, int):
            return str(self.value)
        elif isinstance(self.value, FileSystemPermission) and 'mode' in self.value:
            return str(self.value['mode'])
        else:
            raise ValueError('Invalid input')

    def get_int(self) -> int:
        return file_mode_octal_to_num(self.get_octal())
