from __future__ import annotations

from abc import abstractmethod

from pydantic import BaseModel

from wexample_file.mixin.with_path_mixin import WithPathMixin
from wexample_helpers.const.types import FileStringOrPath


class ItemMixin(WithPathMixin, BaseModel):
    base_path: FileStringOrPath | None = None

    @abstractmethod
    def get_item_title(self) -> str:
        pass

    @abstractmethod
    def is_file(self) -> bool:
        pass

    @abstractmethod
    def is_directory(self) -> bool:
        pass

    def get_octal_mode(self: ItemMixin) -> str:
        from wexample_helpers.helpers.file import file_path_get_octal_mode

        return file_path_get_octal_mode(self.get_path())
