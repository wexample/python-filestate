from __future__ import annotations

from abc import abstractmethod
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class AbstractStateItem(BaseModel):
    path: Optional[Path] = None

    @abstractmethod
    def get_item_title(self) -> str:
        pass

    def get_resolved(self):
        return self.path.resolve()

    @abstractmethod
    def is_file(self) -> bool:
        pass

    @abstractmethod
    def is_directory(self) -> bool:
        pass

    def get_octal_mode(self: AbstractStateItem) -> str:
        from wexample_helpers.helpers.file_helper import file_path_get_octal_mode

        assert self.path is not None

        return file_path_get_octal_mode(self.path)

    def get_path(self) -> Path:
        assert self.path is not None
        return self.path

    def get_path_str(self) -> str:
        return str(self.get_path())
