from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import PrivateAttr

from wexample_filestate.item.mixins.item_mixin import ItemMixin

if TYPE_CHECKING:
    from wexample_file.common.local_file import LocalFile


class ItemFileMixin(ItemMixin):
    _content_cache: Any = PrivateAttr(default=None)

    @property
    def content(self) -> Any:
        return self._content_cache

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
        if reload == True or self._content_cache is None:
            self._content_cache = self.get_local_file().read()
        return self._content_cache

    def write(self, content: Any = None) -> Any:
        return super().write(
            content=self.writable(
                self.override(
                    content=content or self.read()
                )
            )
        )

    def override(self, content: Any = None) -> Any:
        """Let class apply transformations to content, at least before saving."""
        return str(content or self.read())

    def writable(self, content: Any = None) -> str:
        """If needed, transform source content (like dict or class) to a writable format (basically str),
        when using, for instance, default write method. Might be useless if write is overridden.
        """
        return str(content or self.read())
