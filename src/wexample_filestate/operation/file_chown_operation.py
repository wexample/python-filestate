from __future__ import annotations

import os
import subprocess
from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.operation.abstract_operation import AbstractOperation

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope


@base_class
class FileChownOperation(AbstractOperation):
    recursive: bool = public_field(
        description="Apply ownership change recursively",
        default=False,
    )
    target_uid: int | None = public_field(
        description="Target user ID (None = unchanged)",
        default=None,
    )
    target_gid: int | None = public_field(
        description="Target group ID (None = unchanged)",
        default=None,
    )
    _original_uid: int | None = private_field(
        description="Original user ID saved for undo",
    )
    _original_gid: int | None = private_field(
        description="Original group ID saved for undo",
    )

    @classmethod
    def get_scopes(cls) -> list[Scope]:
        from wexample_filestate.enum.scopes import Scope

        return [Scope.OWNERSHIP]

    def apply_operation(self) -> None:
        path = self.target.get_source().get_path()
        stat = os.stat(path)
        self._original_uid = stat.st_uid
        self._original_gid = stat.st_gid

        uid = self.target_uid if self.target_uid is not None else self._original_uid
        gid = self.target_gid if self.target_gid is not None else self._original_gid

        self._run_chown(path=path, uid=uid, gid=gid, recursive=self.recursive)

    def undo(self) -> None:
        assert self._original_uid is not None, "undo() called before apply_operation()"

        path = self.target.get_source().get_path()
        self._run_chown(
            path=path,
            uid=self._original_uid,
            gid=self._original_gid,
            recursive=self.recursive,
        )

    @staticmethod
    def _run_chown(path: os.PathLike, uid: int, gid: int, recursive: bool) -> None:
        cmd = ["sudo", "chown"]
        if recursive:
            cmd.append("-R")
        cmd += [f"{uid}:{gid}", str(path)]
        subprocess.run(cmd, check=True)
