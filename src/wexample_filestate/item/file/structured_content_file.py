from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from wexample_config.const.types import DictConfig
from wexample_filestate.item.item_target_file import ItemTargetFile

if TYPE_CHECKING:
    from wexample_config.config_value.nested_config_value import NestedConfigValue


class StructuredContentFile(ItemTargetFile):
    def read(self, reload: bool = True) -> Any:
        if reload == True or self._content_cache is None:
            self._content_cache = self._parse_file_content(super().read(reload=reload))
        return self._content_cache

    def read_as_config(self) -> NestedConfigValue:
        from wexample_config.config_value.nested_config_value import NestedConfigValue

        return NestedConfigValue(raw=self.read())

    def _parse_file_content(self, content: str) -> Any:
        return content

    def write(self, content: Any) -> Any:
        return super().write(content=self._prepare_content_to_write(content))

    @abstractmethod
    def _prepare_content_to_write(self, content: Any) -> str:
        """If needed, transform source content (like dict or class) to a writable format (basically str),
        when using, for instance, default write method. Might be useless if write is overridden.
        """

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
