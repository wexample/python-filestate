from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_file.mixin.with_local_directory_mixin import WithLocalDirectoryMixin
from wexample_filestate.item.mixins.item_mixin import ItemMixin

if TYPE_CHECKING:
    pass


class ItemDirectoryMixin(WithLocalDirectoryMixin, ItemMixin):
    def get_item_title(self) -> str:
        return "Directory"

    def is_file(self) -> bool:
        return False

    def is_directory(self) -> bool:
        return True
