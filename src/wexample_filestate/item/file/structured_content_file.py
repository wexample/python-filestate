from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import PrivateAttr
from wexample_config.const.types import DictConfig
from wexample_filestate.item.item_target_file import ItemTargetFile
from wexample_helpers.const.types import Scalar

if TYPE_CHECKING:
    from wexample_config.config_value.nested_config_value import NestedConfigValue


class StructuredContentFile(ItemTargetFile):
    # Caches for structured layers
    _parsed_cache: Any | None = PrivateAttr(default=None)
    _content_cache_config: NestedConfigValue | None = PrivateAttr(default=None)

    def read_parsed(self, reload: bool = False, strict: bool = False) -> Any:
        if reload or self._parsed_cache is None:
            text = super().read_text(reload=reload)
            self._parsed_cache = self.loads(text, strict=strict)
            # Invalidate config cache when parsed is reloaded
            if reload:
                self._content_cache_config = None
        return self._parsed_cache

    def read_config(self, reload: bool = False) -> NestedConfigValue:
        if reload:
            self._content_cache_config = None
        if self._content_cache_config is None:
            from copy import deepcopy

            from wexample_config.config_value.nested_config_value import (
                NestedConfigValue,
            )

            parsed = self.read_parsed()
            # Pass a deep copy to avoid any in-place mutation of the shared parsed cache
            self._content_cache_config = NestedConfigValue(raw=deepcopy(parsed))

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

    def write_parsed(self, content: Any | None = None) -> None:
        # If nothing provided, use cache
        if content is None:
            if self._parsed_cache is None:
                raise ValueError("No parsed content to write")
            content = self._parsed_cache
        text = self.dumps(content)
        # Persist via text writer from base mixin
        self.write_text(content=text)
        # Update caches consistently
        self._parsed_cache = content
        self._content_cache_config = None

    def write_config(self, value: NestedConfigValue | None = None) -> None:
        """Write from a NestedConfigValue by converting to raw primitives, then persisting.

        If value is None, uses the cached config. Keeps the config cache aligned after write.
        """
        cfg = value if value is not None else self._content_cache_config
        if cfg is None:
            raise ValueError("No config to write")
        # Delegate normalization to NestedConfigValue
        raw = cfg.to_dict()
        # Write using the parsed pipeline to ensure consistent cache updates
        self.write_parsed(raw)
        # Keep the config cache aligned with what we just wrote
        self._content_cache_config = cfg

    def preview_write(self, content: Any | None = None) -> str:
        """Return the exact text that would be written, accepting either raw text or parsed content, without I/O."""
        if content is None:
            # Use current parsed cache or read from disk without reload
            content = (
                self._parsed_cache
                if self._parsed_cache is not None
                else self.read_parsed(reload=False)
            )
        # If a raw textual payload is provided, parse it first to apply subclass rules/defaults
        if isinstance(content, str):
            content = self.loads(content, strict=False)
        text = self.dumps(content)
        return text

    def preview_write_config(self, value: NestedConfigValue | None = None) -> str:
        """Preview write from a NestedConfigValue without I/O, by dumping its raw representation."""
        cfg = value if value is not None else self._content_cache_config
        if cfg is None:
            # Fallback to parsed preview if no config is available
            return self.preview_write()
        # Delegate normalization to NestedConfigValue
        raw = cfg.to_dict()
        return self.dumps(raw)

    def write_config_value(self, key: str, value: Scalar) -> None:
        """Set a string value at key in the config and persist in one call."""
        cfg = self.read_config()
        cfg.search(key).set_str(str(value))
        self.write_config(cfg)

    def clear(self) -> None:
        super().clear()

        self._parsed_cache = None
        self._content_cache_config = None

    def loads(self, text: str, strict: bool = False) -> Any:
        # Default fallback: return as-is (no parsing). Subclasses should override.
        return text

    def dumps(self, content: Any) -> str:
        # Default fallback: stringify. Subclasses should override for structured formats.
        return str(content)
