from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from wexample_config.const.types import DictConfig
from wexample_filestate.item.item_target_file import ItemTargetFile
from wexample_helpers.const.types import StructuredData
from wexample_helpers_yaml.const.types import YamlContent

if TYPE_CHECKING:
    from wexample_config.config_value.nested_config_value import NestedConfigValue


class StructuredContentFile(ItemTargetFile):
    def read(self) -> YamlContent:
        return self._parse_file_content(super().read())

    def read_as_config(self) -> NestedConfigValue:
        from wexample_config.config_value.nested_config_value import NestedConfigValue

        return NestedConfigValue(raw=self.read())

    @abstractmethod
    def _parse_file_content(self, content: str) -> Any:
        pass

    def write(self, content: StructuredData) -> YamlContent:
        return super().write(content=self._prepare_content_to_write(content))

    @abstractmethod
    def _prepare_content_to_write(self, content: StructuredData) -> str:
        pass

    @abstractmethod
    def _expected_file_name_extension(self) -> str:
        pass

    def prepare_value(self, raw_value: DictConfig | None = None) -> DictConfig:
        expected_extension = self._expected_file_name_extension()

        if expected_extension:
            raw_value = super().prepare_value(raw_value=raw_value)
            from wexample_filestate.config_option.should_have_extension_config_option import (
                ShouldHaveExtensionConfigOption,
            )

            raw_value[ShouldHaveExtensionConfigOption.get_snake_short_class_name()] = (
                self._expected_file_name_extension()
            )

        return raw_value
