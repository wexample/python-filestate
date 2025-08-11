from abc import abstractmethod
from typing import Any

from wexample_filestate.item.item_target_file import ItemTargetFile
from wexample_helpers_yaml.const.types import YamlContent


class StructuredContentFile(ItemTargetFile):
    def read(self) -> YamlContent:
        return self._parse_file_content(
            super().read()
        )

    @abstractmethod
    def _parse_file_content(self, content: str) -> Any:
        pass
