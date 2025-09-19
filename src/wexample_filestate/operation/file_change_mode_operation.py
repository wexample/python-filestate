from __future__ import annotations

from typing import TYPE_CHECKING, cast

from wexample_filestate.operation.abstract_operation import AbstractOperation

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope


class FileChangeModeOperation(AbstractOperation):
    _original_octal_mode: str | None = None
    _recursive: bool = False
    _target_mode: int
    
    def __init__(self, target, target_mode: int, recursive: bool = False, description: str | None = None):
        super().__init__(target=target, description=description)
        self._recursive = recursive
        self._target_mode = target_mode

    @classmethod
    def get_scope(cls) -> Scope:
        from wexample_filestate.enum.scopes import Scope

        return Scope.PERMISSIONS


    def apply(self) -> None:
        from wexample_helpers.helpers.file import (
            file_change_mode,
            file_change_mode_recursive,
        )

        self._original_octal_mode = self.target.get_source().get_octal_mode()

        if self._recursive:
            file_change_mode_recursive(self.target.get_source().get_path(), self._target_mode)
        else:
            file_change_mode(self.target.get_source().get_path(), self._target_mode)

    def undo(self) -> None:
        from wexample_helpers.helpers.file import (
            file_change_mode_recursive,
            file_mode_octal_to_num,
        )

        file_change_mode_recursive(
            self.target.get_source().get_path(),
            file_mode_octal_to_num(self._get_original_octal_mode()),
        )

    def _get_original_octal_mode(self) -> str:
        assert self._original_octal_mode is not None
        return self._original_octal_mode
