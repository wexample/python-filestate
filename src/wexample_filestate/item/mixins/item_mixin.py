from __future__ import annotations

from abc import abstractmethod

from wexample_file.mixin.with_path_mixin import WithPathMixin
from wexample_helpers.classes.field import public_field
from wexample_helpers.const.types import FileStringOrPath
from wexample_helpers.decorator.base_class import base_class


@base_class
class ItemMixin(WithPathMixin):
    base_path: FileStringOrPath | None = public_field(
        description="The original path that will be converted to path", default=None
    )

    @abstractmethod
    def get_item_title(self) -> str:
        pass

    def get_octal_mode(self: ItemMixin) -> str:
        from wexample_helpers.helpers.file import file_path_get_octal_mode

        return file_path_get_octal_mode(self.get_path())

    @abstractmethod
    def is_directory(self) -> bool:
        pass

    @abstractmethod
    def is_file(self) -> bool:
        pass
