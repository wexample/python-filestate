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

    @classmethod
    def _apply_on_empty_content(cls) -> bool:
        """Indicate whether the operation is applicable on empty/whitespace-only files.

        By default, operations are NOT applicable on empty content.
        Subclasses may override to allow applicability on empty files.
        """
        return False

    @staticmethod
    def _is_existing_file(target: TargetFileOrDirectoryType) -> bool:
        local_file = target.get_local_file()
        return target.is_file() and local_file.path.exists()

    @staticmethod
    def _read_current_str_or_fail(target: TargetFileOrDirectoryType) -> str:
        src = AbstractExistingFileOperation._read_current_src(target)
        assert isinstance(src, str)
        return src

    @staticmethod
    def _read_current_non_empty_src(target: TargetFileOrDirectoryType) -> str | None:
        src = AbstractExistingFileOperation._read_current_src(target)
        return src if src is not None and src.strip() != "" else None

    @staticmethod
    def _read_current_src(target: TargetFileOrDirectoryType) -> str | None:
        """Read current file content if it exists; return None if it does not exist."""
        return (
            target.get_local_file().read()
            if AbstractExistingFileOperation._is_existing_file(target)
            else None
        )

    @classmethod
    @abstractmethod
    def preview_source_change(cls, target: TargetFileOrDirectoryType) -> str | None:
        pass

    @classmethod
    def source_need_change(cls, target: TargetFileOrDirectoryType) -> bool:
        # If the file does not exist, do not attempt any change.
        if not cls._is_existing_file(target):
            return False

        # Read the exact current content (may be an empty string).
        current = cls._read_current_src(target)
        assert isinstance(current, str)

        # If current content is empty/whitespace-only and the operation
        # does not apply on empty content, consider "no change needed".
        if current.strip() == "" and not cls._apply_on_empty_content():
            return False

        # If preview is None, consider that as "no change needed".
        preview = cls.preview_source_change(target)
        if preview is None:
            return False

        return preview != current

    def apply(self) -> None:
        changed = self.preview_source_change(self.target)
        if changed is not None:
            self._target_file_write(content=changed)

    def undo(self) -> None:
        self._restore_target_file()
