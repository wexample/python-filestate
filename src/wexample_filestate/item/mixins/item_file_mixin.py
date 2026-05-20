from __future__ import annotations

from typing import Any

from wexample_file.mixin.with_local_file_mixin import WithLocalFileMixin

from wexample_filestate.item.mixins.item_mixin import ItemMixin


class ItemFileMixin(WithLocalFileMixin, ItemMixin):
    # Separate caches for clarity and reliability.
    _bytes_cache: bytes | None = None
    # Disk mtime captured at last cache fill. Used to detect external mutations
    # (subprocess writes, git operations, manual edits) and auto-invalidate caches.
    _cache_mtime_ns: int | None = None
    _text_cache: str | None = None

    @classmethod
    def get_dotted_extension(cls) -> str | None:
        return f".{cls.get_extension()}"

    @classmethod
    def get_extension(cls) -> str:
        return ""

    def clear(self) -> None:
        self.clear_caches()

    def clear_caches(self) -> None:
        self._bytes_cache = None
        self._text_cache = None
        self._cache_mtime_ns = None

    def decode_bytes(self, raw: bytes, encoding: str | None = None) -> str:
        enc = encoding or self.default_encoding()
        return raw.decode(enc)

    def default_encoding(self) -> str:
        return "utf-8"

    def encode_text(self, text: str, encoding: str | None = None) -> bytes:
        enc = encoding or self.default_encoding()
        return text.encode(enc)

    def get_item_title(self) -> str:
        return "File"

    def is_directory(self) -> bool:
        return False

    def is_file(self) -> bool:
        return True

    def preview_write(self, content: Any | None = None) -> str:
        """Generic preview; in base class treats content as text (cast to str if needed)."""
        if content is None:
            return self.preview_write_text()
        if isinstance(content, str):
            return self.preview_write_text(content)
        # Fallback: stringify then apply hooks
        return self.preview_write_text(str(content))

    def preview_write_text(self, content: str | None = None) -> str:
        """Return the exact text that would be written, without performing I/O."""
        # Choose source text: explicit content, cached text, or current file text
        if content is not None:
            return content
        if self._text_cache is not None:
            return self._text_cache
        # Try to read from file, return empty string if file doesn't exist
        try:
            return self.read_text(reload=False)
        except (FileNotFoundError, AttributeError):
            return ""

    def read_bytes(self, reload: bool = False) -> bytes | None:
        stale = self._is_cache_stale()
        if reload or self._bytes_cache is None or stale:
            data = self.get_local_file().read()
            self._cache_mtime_ns = self._get_disk_mtime_ns()
            # LocalFile.read() can return str, bytes, or None if file doesn't exist
            if data is None:
                self._bytes_cache = None
            elif isinstance(data, str):
                # If LocalFile returns text, re-encode using default encoding.
                data = self.encode_text(data)
                self._bytes_cache = data
            else:
                self._bytes_cache = data
            # Invalidate derived caches when content was reloaded from disk.
            if reload or stale:
                self._text_cache = None
                self._on_disk_reload()
        return self._bytes_cache

    def read_text(self, reload: bool = False, encoding: str | None = None) -> str:
        if reload or self._text_cache is None or self._is_cache_stale():
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
        self._cache_mtime_ns = self._get_disk_mtime_ns()

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
        self._cache_mtime_ns = self._get_disk_mtime_ns()

    def _get_disk_mtime_ns(self) -> int | None:
        try:
            return self.get_path().stat().st_mtime_ns
        except (FileNotFoundError, OSError):
            return None

    def _is_cache_stale(self) -> bool:
        result = self.__is_cache_stale_inner()
        try:
            p = str(self.get_path())
        except Exception:
            p = "?"
        if "config.yml" in p or "version.txt" in p or "pyproject.toml" in p:
            import sys

            print(
                f"[STALE-CHECK] path={p} cache_mtime_ns={self._cache_mtime_ns} "
                f"disk_mtime_ns={self._get_disk_mtime_ns()} stale={result} "
                f"text_cached={self._text_cache is not None}",
                file=sys.stderr,
                flush=True,
            )
        return result

    def __is_cache_stale_inner(self) -> bool:
        if self._cache_mtime_ns is None:
            return False
        disk_mtime = self._get_disk_mtime_ns()
        if disk_mtime is None:
            return True
        return disk_mtime > self._cache_mtime_ns

    def _on_disk_reload(self) -> None:
        """Hook for subclasses to clear derived caches when disk content changed."""
