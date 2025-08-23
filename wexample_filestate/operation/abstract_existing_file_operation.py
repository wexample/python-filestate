from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from wexample_filestate.enum.scopes import Scope
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.mixin.file_manipulation_operation_mixin import (
    FileManipulationOperationMixin,
)

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class AbstractExistingFileOperation(FileManipulationOperationMixin, AbstractOperation):
    """Base class for operations that require the target to be an existing file on disk.

    This class only abstracts the existence check (no extension or name check).
    Subclasses remain responsible for option typing/semantics and any extra filters.
    """

    @classmethod
    def get_scope(cls) -> Scope:
        return Scope.CONTENT

    @staticmethod
    def _is_existing_file(target: "TargetFileOrDirectoryType") -> bool:
        local_file = target.get_local_file()
        return target.is_file() and local_file.path.exists()

    @staticmethod
    def _read_current_src(target: "TargetFileOrDirectoryType") -> str:
        """Read current file content if it exists, else return empty string."""
        return target.get_local_file().read() if AbstractExistingFileOperation._is_existing_file(target) else ""

    @abstractmethod
    @classmethod
    def preview_source_change(cls, src: str) -> str:
        """Return updated source if a change is needed, else return original src."""
        raise NotImplementedError
