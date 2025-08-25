from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import PrivateAttr

from wexample_filestate.item.mixins.item_mixin import ItemMixin

if TYPE_CHECKING:
    from wexample_file.common.local_file import LocalFile


class ItemFileMixin(ItemMixin):
    _content_cache: Any = PrivateAttr(default=None)

    def get_item_title(self) -> str:
        return "File"

    def is_file(self) -> bool:
        return True

    def is_directory(self) -> bool:
        return False

    def get_local_file(self) -> LocalFile:
        from wexample_file.common.local_file import LocalFile

        return LocalFile(path=self.get_path())

    def read(self, reload: bool = True) -> Any:
        if not reload and self._content_cache:
            return self._content_cache
        return self.get_local_file().read()

    def write(self, content: str) -> Any:
        return self.get_local_file().write(content)

    def save(self) -> None:
        # Persist cached document with tomlkit round-trip
        if self._content_cache is None:
            # Nothing was changed through this API; no-op
            return
        self.write(self._content_cache)
