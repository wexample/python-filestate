from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import PrivateAttr

from wexample_config.const.types import DictConfig
from wexample_filestate.item.item_target_file import ItemTargetFile

if TYPE_CHECKING:
    from wexample_config.config_value.nested_config_value import NestedConfigValue


class StructuredContentFile(ItemTargetFile):
    # Caches for structured layers
    _parsed_cache: Any | None = PrivateAttr(default=None)
    _content_cache_config: NestedConfigValue | None = PrivateAttr(default=None)

    def read_parsed(self, reload: bool = False, strict: bool = False) -> Any:
        if reload or self._parsed_cache is None:
            text = super().read(reload=reload)
            self._parsed_cache = self.loads(text, strict=strict)
            # Invalidate config cache when parsed is reloaded
            if reload:
                self._content_cache_config = None
        return self._parsed_cache

    def read_config(self) -> NestedConfigValue:
        if self._content_cache_config is None:
            from wexample_config.config_value.nested_config_value import NestedConfigValue
            self._content_cache_config = NestedConfigValue(raw=self.read_parsed())

        return self._content_cache_config

    def _expected_file_name_extension(self) -> str | None:
        return None

    def prepare_value(self, raw_value: DictConfig | None = None) -> DictConfig:
        expected_extension = self._expected_file_name_extension()

        if expected_extension:
            raw_value = super().prepare_value(raw_value=raw_value)
            from wexample_filestate.config_option.should_have_extension_config_option import (
                ShouldHaveExtensionConfigOption,
            )

            raw_value[ShouldHaveExtensionConfigOption.get_snake_short_class_name()] = (
                expected_extension
            )

        return raw_value

    def write_parsed(self, value: Any | None = None) -> None:
        # If nothing provided, use cache
        if value is None:
            if self._parsed_cache is None:
                raise ValueError("No parsed content to write")
            value = self._parsed_cache
        text = self.dumps(value)
        super().write(content=text)
        # Update caches consistently
        self._parsed_cache = value
        self._content_cache_config = None

    def preview_write(self, value: Any | None = None) -> str:
        """Return the exact text that would be written for parsed content, without performing I/O."""
        if value is None:
            # Use current parsed cache or read from disk without reload
            value = self._parsed_cache if self._parsed_cache is not None else self.read_parsed(reload=False)
        text = self.dumps(value)
        return self.before_write_text(text)

    def clear(self):
        super().clear()

        self._parsed_cache = None
        self._content_cache_config = None

    def loads(self, text: str, strict: bool = False) -> Any:
        # Default fallback: return as-is (no parsing). Subclasses should override.
        return text

    def dumps(self, value: Any) -> str:
        # Default fallback: stringify. Subclasses should override for structured formats.
        return str(value)
