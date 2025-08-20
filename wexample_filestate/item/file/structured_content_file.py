from abc import abstractmethod
from typing import Any

from wexample_filestate.item.item_target_file import ItemTargetFile
from wexample_helpers.const.types import StructuredData
from wexample_helpers_yaml.const.types import YamlContent


class StructuredContentFile(ItemTargetFile):
    def read(self) -> YamlContent:
        return self._parse_file_content(
            super().read()
        )

    def read_as_config(self) -> YamlContent:
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
