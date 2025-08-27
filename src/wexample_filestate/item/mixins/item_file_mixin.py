from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import PrivateAttr
from wexample_filestate.item.mixins.item_mixin import ItemMixin

if TYPE_CHECKING:
    from wexample_file.common.local_file import LocalFile


class ItemFileMixin(ItemMixin):
    # Separate caches for clarity and reliability.
    _bytes_cache: bytes | None = PrivateAttr(default=None)
    _text_cache: str | None = PrivateAttr(default=None)

    def get_item_title(self) -> str:
        return "File"

    def is_file(self) -> bool:
        return True

    def is_directory(self) -> bool:
        return False

    def get_local_file(self) -> LocalFile:
        from wexample_file.common.local_file import LocalFile

        return LocalFile(path=self.get_path())

    def default_encoding(self) -> str:
        return "utf-8"

    def decode_bytes(self, raw: bytes, encoding: str | None = None) -> str:
        enc = encoding or self.default_encoding()
        return raw.decode(enc)

    def encode_text(self, text: str, encoding: str | None = None) -> bytes:
        enc = encoding or self.default_encoding()
        return text.encode(enc)

    def read_bytes(self, reload: bool = False) -> bytes:
        if reload or self._bytes_cache is None:
            data = self.get_local_file().read()
            # LocalFile.read() is assumed to return str or bytes. Normalize to bytes.
            if isinstance(data, str):
                # If LocalFile returns text, re-encode using default encoding.
                data = self.encode_text(data)
            self._bytes_cache = data
            # Invalidate text cache if we reloaded from disk.
            if reload:
                self._text_cache = None
        return self._bytes_cache  # type: ignore[return-value]

    def read_text(self, reload: bool = False, encoding: str | None = None) -> str:
        if reload or self._text_cache is None:
            raw = self.read_bytes(reload=reload)
            self._text_cache = self.decode_bytes(raw, encoding=encoding)
        return self._text_cache

    def write_bytes(
        self, content: bytes | None = None, encoding: str | None = None
    ) -> None:
        data = content if content is not None else self._bytes_cache
        if data is None:
            raise ValueError("No bytes content to write")
        # LocalFile exposes a text write API; decode bytes to text first
        text = self.decode_bytes(data, encoding=encoding)
        self.get_local_file().write(
            content=text, encoding=encoding or self.default_encoding()
        )
        # Update caches: keep bytes as source and refresh text from decoded value
        self._bytes_cache = data
        self._text_cache = text

    def write_text(
        self, content: str | None = None, encoding: str | None = None
    ) -> None:
        text = content if content is not None else self._text_cache
        if text is None:
            raise ValueError("No text content to write")
        # Persist to disk using LocalFile text API
        self.get_local_file().write(
            content=text, encoding=encoding or self.default_encoding()
        )
        # Update caches: keep text, refresh bytes from text
        self._text_cache = text
        self._bytes_cache = self.encode_text(text, encoding=encoding)

    def clear(self) -> None:
        self.clear_caches()

    def clear_caches(self) -> None:
        self._bytes_cache = None
        self._text_cache = None

    def preview_write_text(self, content: str | None = None) -> str:
        """Return the exact text that would be written, without performing I/O."""
        # Choose source text: explicit content, cached text, or current file text
        source = (
            content
            if content is not None
            else (
                self._text_cache
                if self._text_cache is not None
                else self.read_text(reload=False)
            )
        )
        return source

    def preview_write(self, content: Any | None = None) -> str:
        """Generic preview; in base class treats content as text (cast to str if needed)."""
        if content is None:
            return self.preview_write_text()
        if isinstance(content, str):
            return self.preview_write_text(content)
        # Fallback: stringify then apply hooks
        return self.preview_write_text(str(content))
