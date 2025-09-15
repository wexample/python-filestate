from __future__ import annotations

from typing import TYPE_CHECKING, cast

from wexample_filestate.operation.abstract_operation import AbstractOperation

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope


class ItemChangeModeOperation(AbstractOperation):
    _original_octal_mode: str | None = None
    _recursive: bool = False
    
    def __init__(self, target, recursive: bool = False):
        super().__init__(target=target)
        self._recursive = recursive

    @classmethod
    def get_scope(cls) -> Scope:
        from wexample_filestate.enum.scopes import Scope

        return Scope.PERMISSIONS


    def apply(self) -> None:
        from wexample_filestate.option.mode_option import ModeOption
        from wexample_helpers.helpers.file import (
            file_change_mode,
            file_change_mode_recursive,
        )

        self._original_octal_mode = self.target.get_source().get_octal_mode()
        mode_int = cast(
            ModeOption, self.target.get_option(ModeOption)
        ).get_int()

        if self._recursive:
            file_change_mode_recursive(self.target.get_source().get_path(), mode_int)
        else:
            file_change_mode(self.target.get_source().get_path(), mode_int)

    def describe_after(self) -> str:
        from wexample_filestate.option.mode_option import ModeOption

        path = self.target.get_path().as_posix()
        target_octal = self.target.get_option_value(ModeOption).get_str()
        return f"Permissions for '{path}' are now set to {target_octal}."

    def describe_before(self) -> str:
        from wexample_filestate.option.mode_option import ModeOption

        current_octal = self.target.get_source().get_octal_mode()
        target_octal = self.target.get_option_value(ModeOption).get_str()
        path = self.target.get_path().as_posix()
        return f"The item '{path}' has permissions {current_octal} but should be {target_octal}. Permissions will be updated."

    def description(self) -> str:
        return "Ensure file or directory permissions match the configured mode."

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
