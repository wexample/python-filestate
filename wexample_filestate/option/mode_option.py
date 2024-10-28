from typing import Union

from wexample_filestate.const.files import FileSystemPermission
from wexample_config.option.abstract_option import AbstractOption
from wexample_helpers.helpers.file_helper import file_mode_octal_to_num


class ModeOption(AbstractOption):
    @staticmethod
    def get_value_type() -> FileSystemPermission:
        return Union[str, int, FileSystemPermission]

    def get_octal(self) -> str:
        if self.value.is_str():
            return self.value.get_str()
        elif self.value.is_int():
            return self.value.to_str()
        elif isinstance(self.value, FileSystemPermission) and 'mode' in self.value:
            return str(self.value['mode'])
        else:
            raise ValueError(f"Unexpected value in get_octal: {self.value}")

    def get_int(self) -> int:
        return file_mode_octal_to_num(self.get_octal())
