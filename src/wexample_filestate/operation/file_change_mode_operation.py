from __future__ import annotations

import os
from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.file_chown_operation import FileChownOperation

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope


@base_class
class FileChangeModeOperation(AbstractOperation):
    recursive: bool = public_field(
        description="Apply mode to child list",
    )
    target_gid: int | None = public_field(
        description="Target group ID to apply alongside chmod (None = no chown)",
        default=None,
    )
    target_mode: bool = public_field(
        description="The permissions mode to apply",
    )
    target_uid: int | None = public_field(
        description="Target user ID to apply alongside chmod (None = no chown)",
        default=None,
    )
    _original_gid: int | None = private_field(
        description="Cached gid to provide undo",
    )
    _original_octal_mode: str | None = private_field(
        description="Cached mode to provide undo"
    )
    _original_uid: int | None = private_field(
        description="Cached uid to provide undo",
    )

    @classmethod
    def get_scopes(cls) -> [Scope]:
        from wexample_filestate.enum.scopes import Scope

        return [Scope.PERMISSIONS, Scope.OWNERSHIP]

    def apply_operation(self) -> None:
        import pwd

        from wexample_helpers.helpers.file import (
            file_change_mode,
            file_change_mode_recursive,
        )

        source = self.target.get_source()
        path = source.get_path()

        if path.is_symlink():
            return

        self._original_octal_mode = source.get_octal_mode()

        # chown first so that if the file is owned by another user, we acquire
        # ownership before attempting chmod (chmod requires owning the file).
        if self.target_uid is not None or self.target_gid is not None:
            stat = os.stat(path)
            self._original_uid = stat.st_uid
            self._original_gid = stat.st_gid
            uid = self.target_uid if self.target_uid is not None else self._original_uid
            gid = self.target_gid if self.target_gid is not None else self._original_gid
            FileChownOperation._run_chown(
                path=path, uid=uid, gid=gid, recursive=self.recursive
            )

        try:
            if self.recursive:
                file_change_mode_recursive(path, self.target_mode)
            else:
                file_change_mode(path, self.target_mode)
        except PermissionError:
            try:
                owner = pwd.getpwuid(path.stat().st_uid).pw_name
            except Exception:
                owner = "unknown"
            raise PermissionError(
                f"Cannot change permissions on '{path}' (owned by '{owner}'). "
                f"Fix with: sudo chmod 755 '{path}'"
            )

    def undo(self) -> None:
        from wexample_helpers.helpers.file import (
            file_change_mode_recursive,
            file_mode_octal_to_num,
        )

        path = self.target.get_source().get_path()

        file_change_mode_recursive(
            path,
            file_mode_octal_to_num(self._get_original_octal_mode()),
        )

        if self._original_uid is not None:
            FileChownOperation._run_chown(
                path=path,
                uid=self._original_uid,
                gid=self._original_gid,
                recursive=self.recursive,
            )

    def _get_original_octal_mode(self) -> str:
        assert self._original_octal_mode is not None
        return self._original_octal_mode
