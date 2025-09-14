from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.mixin.file_manipulation_operation_mixin import (
    FileManipulationOperationMixin,
)
from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.enum.scopes import Scope


@base_class
class AbstractExistingFileOperation(FileManipulationOperationMixin, AbstractOperation):
    """Base class for operations that require the target to be an existing file on disk.

    This class only abstracts the existence check (no extension or name check).
    Subclasses remain responsible for option typing/semantics and any extra filters.
    """

    _changed_source: str | None = private_field(
        default=None,
        description="Internal storage for a modified source string, if any",
    )
    _source_need_change: bool | None = private_field(
        default=None,
        description="Flag indicating whether the source requires modification",
    )

    @classmethod
    def get_scope(cls) -> Scope:
        from wexample_filestate.enum.scopes import Scope

        return Scope.CONTENT

    @classmethod
    @abstract_method
    def preview_source_change(cls, target: TargetFileOrDirectoryType) -> str | None:
        pass

    @classmethod
    def _apply_on_empty_content(cls) -> bool:
        """Indicate whether the operation is applicable on empty/whitespace-only files.

        By default, operations are NOT applicable on empty content.
        Subclasses may override to allow applicability on empty files.
        """
        return False

    @staticmethod
    def _is_existing_file(target: TargetFileOrDirectoryType) -> bool:
        if not target.source or not target.is_file():
            return False
        return target.get_local_file().path.exists()

    @classmethod
    def _read_current_non_empty_src(cls,target: TargetFileOrDirectoryType) -> str | None:
        src = cls._read_current_src(target)
        return src if src is not None and src.strip() != "" else None

    @staticmethod
    def _read_current_src(target: TargetFileOrDirectoryType) -> str | None:
        """Read current file content if it exists; return None if it does not exist."""
        return target.get_local_file().read()

    @classmethod
    def _read_current_str_or_fail(cls,target: TargetFileOrDirectoryType) -> str:
        src = cls._read_current_src(target)
        assert isinstance(src, str)
        return src

    def apply(self) -> None:
        if self._changed_source is not None:
            self._target_file_write(content=self._changed_source)

    def source_need_change(self, target: TargetFileOrDirectoryType) -> bool:
        if self._source_need_change is not None:
            return self._source_need_change

        # If the file does not exist, do not attempt any change.
        if not self._is_existing_file(target):
            return False

        # Read the exact current content (may be an empty string).
        current = self._read_current_src(target)
        assert isinstance(current, str)

        # If current content is empty/whitespace-only and the operation
        # does not apply on empty content, consider "no change needed".
        if current.strip() == "" and not self._apply_on_empty_content():
            return False

        # If preview is None, consider that as "no change needed".
        if self._changed_source is None:
            self._changed_source = self.preview_source_change(target)
        if self._changed_source is None:
            return False

        self._source_need_change = self._changed_source != current
        return self._source_need_change

    def undo(self) -> None:
        self._restore_target_file()
